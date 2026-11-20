import os
import cv2
import uuid
import numpy as np
import torch
import threading
from flask import current_app
from app.ai_core import registry

# Because we use a Singleton PyTorch model, we must lock it during backward passes 
# to prevent race conditions when multiple users run analyses simultaneously.
gradcam_lock = threading.Lock()

class GradCAMExtractor:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.forward_handle = None
        self.backward_handle = None

    def save_activation(self, module, input, output):
        self.activations = output

    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]
        
    def register_hooks(self):
        # Register hooks dynamically to avoid permanent memory footprint
        self.forward_handle = self.target_layer.register_forward_hook(self.save_activation)
        self.backward_handle = self.target_layer.register_full_backward_hook(self.save_gradient)
        
    def remove_hooks(self):
        if self.forward_handle:
            self.forward_handle.remove()
        if self.backward_handle:
            self.backward_handle.remove()

def generate_disease_heatmap(image_path: str, variety_encoded: int, age_scaled: float, predicted_class_idx: int) -> str:
    """
    Generates a Grad-CAM heatmap for the EfficientNet-B3 disease model.
    Saves the image to the static heatmaps folder and returns the relative URL.
    """
    model = registry.models.get('disease')
    if model is None:
        return ""

    # Prevent thread collisions during gradient calculation
    with gradcam_lock:
        try:
            # 1. Preprocess Image (Matches training pipeline)
            original_img = cv2.imread(image_path)
            if original_img is None:
                return ""
                
            img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (300, 300))
            img_normalized = img / 255.0
            img_normalized = (img_normalized - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
            img_transposed = np.transpose(img_normalized, (2, 0, 1))
            
            img_tensor = torch.tensor(img_transposed, dtype=torch.float32).unsqueeze(0).to(registry.device)
            tab_tensor = torch.tensor([[variety_encoded, age_scaled]], dtype=torch.float32).to(registry.device)
            
            # Extract target layer (EfficientNet-B3 specific)
            target_layer = model.backbone.conv_head
            extractor = GradCAMExtractor(model, target_layer)
            extractor.register_hooks()
            
            # 2. Forward Pass
            model.zero_grad()
            output = model(img_tensor, tab_tensor)
            
            # 3. Backward Pass on the predicted class
            target = output[0, predicted_class_idx]
            target.backward(retain_graph=False)
            
            gradients = extractor.gradients.data.cpu().numpy()[0]
            activations = extractor.activations.data.cpu().numpy()[0]
            
            weights = np.mean(gradients, axis=(1, 2))
            cam = np.zeros(activations.shape[1:], dtype=np.float32)
            
            for i, w in enumerate(weights):
                cam += w * activations[i]
                
            # ReLU on CAM (we only care about features with a positive influence)
            cam = np.maximum(cam, 0)
            cam = cv2.resize(cam, (original_img.shape[1], original_img.shape[0]))
            
            # Normalize CAM
            cam_max = np.max(cam)
            if cam_max != 0:
                cam = cam / cam_max
                
            # 4. Generate Heatmap Overlay
            heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
            heatmap = np.float32(heatmap) / 255
            original_float = np.float32(original_img) / 255
            
            overlay = 0.5 * heatmap + 0.5 * original_float
            overlay = np.uint8(255 * overlay)
            
            filename = f"heatmap_{uuid.uuid4().hex}.jpg"
            heatmap_dir = current_app.config.get('HEATMAP_FOLDER', 'app/static/heatmaps')
            filepath = os.path.join(heatmap_dir, filename)
            
            cv2.imwrite(filepath, overlay)
            
            # Return relative path for frontend rendering
            return f"/static/heatmaps/{filename}"
            
        except Exception as e:
            print(f"Grad-CAM Error: {e}")
            return ""
        finally:
            # Always remove hooks to prevent memory leaks
            if 'extractor' in locals():
                extractor.remove_hooks()
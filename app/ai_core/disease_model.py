import torch
import torch.nn as nn
import timm
import cv2
import numpy as np
from PIL import Image
from . import registry

class MultiModalEfficientNet(nn.Module):
    """
    Architecture matching Phase 1.1.
    Combines EfficientNet-B3 for the leaf image with dense layers for age and variety.
    """
    def __init__(self, num_classes=10, num_varieties=10, pretrained=False):
        super().__init__()
        # Load backbone without head
        self.backbone = timm.create_model('tf_efficientnet_b3.ns_jft_in1k', pretrained=pretrained, num_classes=0)
        num_image_features = self.backbone.num_features
        
        # Tabular embeddings
        self.variety_embedding = nn.Embedding(num_embeddings=num_varieties, embedding_dim=16)
        self.tabular_fc = nn.Sequential(
            nn.Linear(16 + 1, 32),
            nn.BatchNorm1d(32),
            nn.SiLU(),
            nn.Dropout(0.2)
        )
        
        # Combined classifier
        self.classifier = nn.Sequential(
            nn.Linear(num_image_features + 32, 512),
            nn.BatchNorm1d(512),
            nn.SiLU(),
            nn.Dropout(0.4),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, image, tabular):
        img_features = self.backbone(image)
        variety = tabular[:, 0].long()
        age = tabular[:, 1].unsqueeze(1)
        
        var_emb = self.variety_embedding(variety)
        tab_features = torch.cat([var_emb, age], dim=1)
        tab_features = self.tabular_fc(tab_features)
        
        combined = torch.cat([img_features, tab_features], dim=1)
        return self.classifier(combined)

def predict_disease(image_path: str, variety_encoded: int, age_scaled: float) -> dict:
    """
    Runs inference on the uploaded leaf image using the EfficientNet model.
    """
    model = registry.models.get('disease')
    if model is None:
        return {"disease": "Unknown (Model Not Loaded)", "confidence": 0.0, "class_idx": 0}
        
    class_names = [
        "Bacterial Leaf Blight", "Bacterial Panicle Blight", "Blast", "Brown Spot", 
        "Dead Heart", "Downy Mildew", "Hispa", "Normal", "Neck Blast", "Tungro"
    ]

    try:
        # Preprocess Image (matching Phase 1.1 Albumentations pipeline)
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))
        img = img / 255.0
        # ImageNet normalization
        img = (img - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
        img = np.transpose(img, (2, 0, 1)) # HWC to CHW
        
        img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0).to(registry.device)
        tab_tensor = torch.tensor([[variety_encoded, age_scaled]], dtype=torch.float32).to(registry.device)

        # Inference
        with torch.no_grad():
            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                output = model(img_tensor, tab_tensor)
                probs = torch.nn.functional.softmax(output, dim=1)[0]
                
        confidence, class_idx = torch.max(probs, dim=0)
        
        return {
            "disease": class_names[class_idx.item()],
            "confidence": round(confidence.item() * 100, 2),
            "class_idx": class_idx.item()
        }
    except Exception as e:
        return {"error": str(e)}
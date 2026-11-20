import os
import cv2
from . import registry

def predict_pest(image_path: str) -> dict:
    """
    Runs YOLOv8 object detection to find pests on the leaf image.
    Returns the highest confidence pest and its bounding box for UI rendering.
    """
    model = registry.models.get('pest')
    if model is None:
        return {"pest": "Unknown (Model Not Loaded)", "confidence": 0.0, "risk_score": "Unknown", "bbox": None}
        
    try:
        # Inference using Ultralytics API
        # conf=0.25 removes extremely low confidence background noise
        results = model.predict(source=image_path, imgsz=416, conf=0.25, verbose=False)
        
        result = results[0]
        
        # If no pests are detected
        if len(result.boxes) == 0:
            return {
                "pest": "No Pest Detected",
                "confidence": 100.0,
                "risk_score": "Low",
                "bbox": None
            }
            
        # Get the highest confidence detection
        best_box = result.boxes[0]
        for box in result.boxes:
            if box.conf[0] > best_box.conf[0]:
                best_box = box
                
        pest_class_id = int(best_box.cls[0].item())
        confidence = float(best_box.conf[0].item())
        
        # Convert bbox [x1, y1, x2, y2] to a list of ints for JSON serialization
        bbox = best_box.xyxy[0].cpu().numpy().astype(int).tolist()
        
        pest_name = result.names[pest_class_id]
        
        # Simple risk mapping based on confidence
        risk = "High" if confidence > 0.75 else "Medium"
        
        return {
            "pest": pest_name.title(),
            "confidence": round(confidence * 100, 2),
            "risk_score": risk,
            "bbox": bbox
        }
        
    except Exception as e:
        return {"error": str(e)}
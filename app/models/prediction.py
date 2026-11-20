from datetime import datetime
from app.database.db_setup import db

class Prediction(db.Model):
    """
    The central hub storing all outputs from the 5 AI models, 
    calculated scores, and paths to XAI heatmaps.
    """
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    input_id = db.Column(db.Integer, db.ForeignKey('field_inputs.id'), nullable=False, unique=True)
    
    # EfficientNet Output
    disease_label = db.Column(db.String(100), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    
    # XGBoost Nutrient Output
    nutrient_status = db.Column(db.String(100), nullable=True)
    
    # YOLOv8 Output
    pest_type = db.Column(db.String(100), nullable=True)
    pest_risk_score = db.Column(db.String(50), nullable=True) # e.g., "High", "Medium"
    
    # XGBoost Irrigation Output
    irrigation_requirement = db.Column(db.Float, nullable=True) # mm/day
    
    # LightGBM Yield Output
    yield_forecast = db.Column(db.Float, nullable=True) # tons/hectare
    expected_profit = db.Column(db.Float, nullable=True) # calculated dynamically at inference
    
    # Calculated Scores
    sustainability_score = db.Column(db.Integer, nullable=True) # 0-100 scale
    
    # Paths & JSON Payloads
    heatmap_path = db.Column(db.String(255), nullable=True) # Relative path to Grad-CAM image
    weather_impact_json = db.Column(db.JSON, nullable=True) # LSTM 7-day risk array
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Prediction ID:{self.id} for Input:{self.input_id}>"
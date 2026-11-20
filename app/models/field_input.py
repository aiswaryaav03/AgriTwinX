from datetime import datetime
from app.database.db_setup import db

class FieldInput(db.Model):
    """
    Stores the raw data submitted by the farmer via the 'Analyse My Field' form.
    This data acts as the input for all 5 AI models.
    """
    __tablename__ = 'field_inputs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Crop details
    crop_age = db.Column(db.Integer, nullable=False) # In days
    variety = db.Column(db.String(50), nullable=False)
    growth_stage = db.Column(db.String(50), nullable=False)
    
    # Soil parameters (N, P, K, pH)
    soil_N = db.Column(db.Float, nullable=False)
    soil_P = db.Column(db.Float, nullable=False)
    soil_K = db.Column(db.Float, nullable=False)
    soil_pH = db.Column(db.Float, nullable=False)
    
    # Current season chemical usage
    fertilizer_used = db.Column(db.Float, nullable=False) # In kg
    pesticide_used = db.Column(db.Float, nullable=False) # In kg
    
    input_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    # One-to-One relationship with Prediction
    prediction = db.relationship('Prediction', backref='input_data', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<FieldInput ID:{self.id} for User:{self.user_id}>"
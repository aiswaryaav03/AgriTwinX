from datetime import datetime
from app.database.db_setup import db

class MarketPrice(db.Model):
    """
    Global configuration table managed by the Admin.
    Used dynamically by the LightGBM yield model to calculate accurate financial returns.
    """
    __tablename__ = 'market_prices'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(50), unique=True, nullable=False)
    price_per_ton = db.Column(db.Float, nullable=False) # e.g., 18500.00
    
    # Optional field to track which admin made the update, assuming a single admin role
    updated_by_admin = db.Column(db.String(100), nullable=True, default="System Admin") 
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<MarketPrice {self.crop_name}: ₹{self.price_per_ton}>"
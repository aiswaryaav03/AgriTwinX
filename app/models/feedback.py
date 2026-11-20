from datetime import datetime
from app.database.db_setup import db

class Feedback(db.Model):
    """
    Captures post-harvest ground-truth data from the farmer.
    Crucial for continuous monitoring and future model retraining by the Admin.
    """
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    actual_yield = db.Column(db.Float, nullable=False) # Realized tons/hectare
    disease_confirmed = db.Column(db.String(100), nullable=True) # Was the AI correct?
    treatment_used = db.Column(db.String(255), nullable=True)
    
    was_helpful = db.Column(db.Boolean, nullable=False, default=True)
    
    harvest_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Feedback ID:{self.id} from User:{self.user_id}>"
from datetime import datetime
from app.database.db_setup import db

class TreatmentLog(db.Model):
    """
    Logs the user's interaction with the Treatment Simulator module
    and the resulting Groq LLaMA 3 comparative analysis.
    """
    __tablename__ = 'treatment_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    disease = db.Column(db.String(100), nullable=False)
    treatment_chosen = db.Column(db.String(255), nullable=False) # e.g., "Tricyclazole Spray vs Neem Oil"
    
    # Store the parsed LLM response to avoid re-querying the API for history views
    groq_response_json = db.Column(db.JSON, nullable=False) 
    
    action_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<TreatmentLog ID:{self.id} User:{self.user_id} Disease:{self.disease}>"
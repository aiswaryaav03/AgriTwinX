from datetime import datetime
from app.database.db_setup import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """
    Represents a registered farmer in the AgriTwinX platform.
    Inherits from UserMixin to integrate seamlessly with Flask-Login.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    village = db.Column(db.String(100), nullable=False)
    farm_size = db.Column(db.Float, nullable=False) # In acres
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # One-to-Many Relationships
    field_inputs = db.relationship('FieldInput', backref='farmer', lazy=True, cascade="all, delete-orphan")
    predictions = db.relationship('Prediction', backref='farmer', lazy=True, cascade="all, delete-orphan")
    treatment_logs = db.relationship('TreatmentLog', backref='farmer', lazy=True, cascade="all, delete-orphan")
    calendars = db.relationship('FarmingCalendar', backref='farmer', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', backref='farmer', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name} - {self.village}>"
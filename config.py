import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration with shared variables across all environments."""
    
    # Security & Authentication
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # External APIs
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    
    # File Upload Paths & Limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    HEATMAP_FOLDER = os.path.join(basedir, 'app', 'static', 'heatmaps')
    AI_WEIGHTS_FOLDER = os.path.join(basedir, 'ai_weights')
    
    # Database Settings (Fallback for SQLAlchemy)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration using local SQLite."""
    DEBUG = True
    # Default to instance/agritwinx.db if not specified
    DB_PATH = os.path.abspath(os.path.join(basedir, "instance", "agritwinx.db"))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or f"sqlite:///{DB_PATH.replace(os.sep, '/')}"
class ProductionConfig(Config):
    """Production configuration using PostgreSQL."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
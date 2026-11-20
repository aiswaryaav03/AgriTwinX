import os
from flask import Flask
from flask_login import LoginManager
from .database.db_setup import db
from .models.user import User

# Import Blueprints
from .routes.auth_routes import auth_bp
from .routes.farmer_routes import farmer_bp
from .routes.admin_routes import admin_bp
from .routes.api_routes import api_bp
from flask import redirect, url_for
from flask import render_template


def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Import the config dictionary from the root config.py
    from config import config_dict
    app.config.from_object(config_dict[config_name])
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['HEATMAP_FOLDER'], exist_ok=True)
    os.makedirs(app.config.get('AI_WEIGHTS_FOLDER', 'ai_weights'), exist_ok=True)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(farmer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def home():
        return render_template("index.html")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30} -> {rule}")
    print("=============================\n")
    return app
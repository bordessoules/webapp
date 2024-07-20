# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)    
    db.init_app(app)    
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    with app.app_context():
        from app import models  # Import models here
        db.create_all()
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
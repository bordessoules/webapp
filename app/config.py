# app/config.py
import os

class Config:
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///items.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Use environment variable in production
    UPLOAD_FOLDER =  'uploads'
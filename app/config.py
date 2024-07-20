# app/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'items.db')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///items.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Use environment variable in production
    UPLOAD_FOLDER =  'uploads'
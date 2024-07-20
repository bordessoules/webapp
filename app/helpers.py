import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    
    :param filename: Filename to check
    :return: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    """
    Generate a unique filename while preserving the original file extension.
    
    :param filename: Original filename
    :return: Unique filename
    """
    # Get the file extension
    _, file_extension = os.path.splitext(filename)
    
    # Generate a unique filename using UUID
    unique_filename = str(uuid.uuid4()) + file_extension
    # Ensure the filename is secure
    return secure_filename(unique_filename)


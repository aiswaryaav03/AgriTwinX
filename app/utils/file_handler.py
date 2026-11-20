import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename: str) -> bool:
    """Checks if the uploaded file has a permitted extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_image(file: FileStorage, upload_folder: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Secures and saves an uploaded image file using a UUID to prevent collisions.
    
    Args:
        file (FileStorage): The uploaded file object from Flask's request.files.
        upload_folder (str): The absolute path to the directory where images are stored.
        
    Returns:
        Tuple containing:
        - absolute_path (str): For backend OpenCV/PIL processing.
        - relative_path (str): For frontend HTML rendering.
        Returns (None, None) if saving fails.
    """
    if file and file.filename and allowed_file(file.filename):
        try:
            # Secure the original filename and split extension
            original_filename = secure_filename(file.filename)
            ext = original_filename.rsplit('.', 1)[1].lower()
            
            # Generate a unique filename using UUID4
            unique_filename = f"leaf_{uuid.uuid4().hex}.{ext}"
            absolute_path = os.path.join(upload_folder, unique_filename)
            
            # Save the file to disk
            file.save(absolute_path)
            
            # Generate the relative path for the frontend (assuming standard static routing)
            relative_path = f"/static/uploads/{unique_filename}"
            
            return absolute_path, relative_path
            
        except Exception as e:
            logger.error(f"Failed to save uploaded image: {e}")
            return None, None
            
    return None, None
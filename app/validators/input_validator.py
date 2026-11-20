import logging
from typing import Dict, Tuple, Any
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)

def validate_analysis_input(form_data: Dict[str, Any], files_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates the multipart form data submitted from the 'Analyse My Field' dashboard.
    Ensures all expected parameters are present, within logical bounds, and safely cast.
    
    Returns:
        Tuple containing:
        - is_valid (bool): True if validation passes, False otherwise.
        - error_message (str): Descriptive error if validation fails, empty string otherwise.
        - sanitized_data (dict): Cleaned and cast data ready for processing.
    """
    sanitized = {}

    # 1. Validate Image
    if 'image' not in files_data:
        return False, "Leaf image is required.", {}
        
    image_file = files_data['image']
    if not isinstance(image_file, FileStorage) or image_file.filename == '':
        return False, "Invalid leaf image file provided.", {}

    # 2. Validate Crop Parameters
    try:
        sanitized['crop_age'] = int(form_data.get('crop_age', 45))
        if not (1 <= sanitized['crop_age'] <= 180):
            return False, "Crop age must be between 1 and 180 days.", {}
            
        sanitized['variety'] = str(form_data.get('variety', 'IR-64')).strip()
        sanitized['growth_stage'] = str(form_data.get('growth_stage', 'Tillering')).strip()
        
    except ValueError:
        return False, "Invalid format for crop age.", {}

    # 3. Validate Farm and Chemical Data
    try:
        sanitized['farm_size'] = float(form_data.get('farm_size', 1.0))
        if sanitized['farm_size'] <= 0:
            return False, "Farm size must be greater than 0.", {}
            
        sanitized['location'] = str(form_data.get('location', '')).strip()
        
        sanitized['fertilizer_used'] = float(form_data.get('fertilizer_used', 0.0))
        sanitized['pesticide_used'] = float(form_data.get('pesticide_used', 0.0))
        if sanitized['fertilizer_used'] < 0 or sanitized['pesticide_used'] < 0:
            return False, "Chemical usage amounts cannot be negative.", {}
            
    except ValueError:
        return False, "Invalid format for farm size or chemical inputs.", {}

    # 4. Validate Soil Data (Optional, falls back to regional defaults if missing)
    try:
        soil_N = form_data.get('soil_N')
        soil_P = form_data.get('soil_P')
        soil_K = form_data.get('soil_K')
        soil_pH = form_data.get('soil_pH')
        
        if all(v is not None and str(v).strip() != '' for v in [soil_N, soil_P, soil_K, soil_pH]):
            sanitized['soil_N'] = float(soil_N)
            sanitized['soil_P'] = float(soil_P)
            sanitized['soil_K'] = float(soil_K)
            sanitized['soil_pH'] = float(soil_pH)
            
            # Bound checks for soil
            if not (0 <= sanitized['soil_N'] <= 500):
                return False, "Soil Nitrogen (N) is out of expected logical bounds (0-500).", {}
            if not (0 <= sanitized['soil_P'] <= 200):
                return False, "Soil Phosphorus (P) is out of expected logical bounds (0-200).", {}
            if not (0 <= sanitized['soil_K'] <= 300):
                return False, "Soil Potassium (K) is out of expected logical bounds (0-300).", {}
            if not (0.0 <= sanitized['soil_pH'] <= 14.0):
                return False, "Soil pH must be between 0 and 14.", {}
        else:
            # Leave as None to trigger regional defaults logic in the API route
            sanitized['soil_N'] = None
            sanitized['soil_P'] = None
            sanitized['soil_K'] = None
            sanitized['soil_pH'] = None
            
    except ValueError:
        return False, "Soil parameters must be valid numeric values.", {}

    return True, "", sanitized
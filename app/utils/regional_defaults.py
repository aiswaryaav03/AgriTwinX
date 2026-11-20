import logging

logger = logging.getLogger(__name__)

# In a full production environment, this could be a query to a larger GIS database.
# For now, it provides robust generic fallbacks for major Indian paddy-producing states.
REGIONAL_SOIL_DATA = {
    "tamil nadu": {"N": 80.0, "P": 40.0, "K": 35.0, "pH": 6.5},
    "thanjavur": {"N": 82.0, "P": 42.0, "K": 36.0, "pH": 6.6}, # Specific highly-active paddy region
    "punjab": {"N": 100.0, "P": 30.0, "K": 30.0, "pH": 7.5},
    "haryana": {"N": 95.0, "P": 32.0, "K": 31.0, "pH": 7.8},
    "west bengal": {"N": 70.0, "P": 45.0, "K": 40.0, "pH": 5.8},
    "andhra pradesh": {"N": 85.0, "P": 38.0, "K": 34.0, "pH": 6.8},
    "uttar pradesh": {"N": 90.0, "P": 35.0, "K": 32.0, "pH": 7.2},
    "kerala": {"N": 65.0, "P": 35.0, "K": 25.0, "pH": 5.5},
    "generic": {"N": 80.0, "P": 40.0, "K": 35.0, "pH": 6.5}
}

def get_soil_defaults(location_string: str) -> dict:
    """
    Attempts to match the user's location string against known regional soil averages.
    This acts as a fallback when the farmer selects "Use Regional Average".
    
    Args:
        location_string (str): The village/district/state provided by the user.
        
    Returns:
        dict: Containing 'N', 'P', 'K', and 'pH' values.
    """
    if not location_string:
        logger.warning("Empty location provided for soil defaults. Using generic.")
        return REGIONAL_SOIL_DATA["generic"]
        
    location_lower = location_string.lower()
    
    # Simple substring matching for regions
    for region, defaults in REGIONAL_SOIL_DATA.items():
        if region != "generic" and region in location_lower:
            logger.info(f"Matched location '{location_string}' to region '{region}'. Using regional soil defaults.")
            return defaults
            
    logger.info(f"Could not match location '{location_string}' to a specific region. Using generic average.")
    return REGIONAL_SOIL_DATA["generic"]
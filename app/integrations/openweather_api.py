import requests
import logging
import numpy as np
from flask import current_app
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_fallback_weather_data() -> dict:
    """
    Provides safe, realistic fallback data for Thanjavur, Tamil Nadu 
    if the OpenWeatherMap API fails or the key is missing.
    Ensures the 5 AI models never crash due to network issues.
    """
    # Create a 168-hour (7-day) sequence of realistic dummy data for the LSTM
    # Features: ['Temp (C)', 'Humidity', 'Wind Speed', 'Wind Bearing', 'Pressure', 'Precip Type']
    # Precip Type Encoded: 0 = None, 1 = Rain
    fallback_sequence = np.zeros((168, 6))
    for i in range(168):
        fallback_sequence[i] = [
            32.0 + np.sin(i / 24.0 * 2 * np.pi) * 4, # Temp oscillating between 28-36
            75.0 + np.cos(i / 24.0 * 2 * np.pi) * 15, # Humidity oscillating
            12.0,   # Wind speed
            180.0,  # Wind bearing
            1010.0, # Pressure
            0.0     # Precip Type (None)
        ]
        
    return {
        "temperature": 34.5,
        "humidity": 82.0,
        "current_rainfall": 0.0,
        "annual_rainfall": 1050.0, # Approximate for TN
        "weather_sequence_7_days": fallback_sequence,
        "status": "fallback_used"
    }


def fetch_weather_data(location_name: str) -> dict:
    """
    Fetches current weather and 7-day hourly forecast from OpenWeatherMap.
    Formats the data specifically for the XGBoost, LightGBM, and LSTM models.
    """
    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    if not api_key or api_key == 'your_openweathermap_api_key_here':
        logger.warning("OpenWeatherMap API key missing or default. Using fallback data.")
        return _get_fallback_weather_data()

    try:
        # 1. Geocode the location name to Lat/Lon
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=1&appid={api_key}"
        geo_resp = requests.get(geocode_url, timeout=5)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        
        if not geo_data:
            logger.error(f"Could not geocode location: {location_name}")
            return _get_fallback_weather_data()
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']


        # 2. Fetch Weather Data (Using One Call API or 5 Day / 3 Hour forecast simulated to hourly)
        # Note: Standard free tier uses forecast endpoint. We'll adapt it to build the LSTM sequence.
        weather_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        weather_resp = requests.get(weather_url, timeout=5)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        current_list = weather_data.get('list', [])
        if not current_list:
            return _get_fallback_weather_data()

        # Extract current metrics for XGBoost models
        current_temp = current_list[0]['main']['temp']
        current_humidity = current_list[0]['main']['humidity']
        
        # Rainfall in last 3 hours (if any)
        rain_3h = current_list[0].get('rain', {}).get('3h', 0.0)
        current_rainfall = rain_3h / 3.0 # Approximate per hour

        # 3. Build the 168-hour sequence for the LSTM
        # The free API gives 40 timestamps (5 days * 8 intervals/day).
        # We will interpolate this into a 168-hour continuous sequence to satisfy the LSTM input shape.
        lstm_sequence = np.zeros((168, 6))
        
        for hour in range(168):
            # Map the 168 hours to the nearest available 3-hour forecast block
            block_idx = min(hour // 3, len(current_list) - 1)
            block = current_list[block_idx]
            
            temp = block['main']['temp']
            hum = block['main']['humidity']
            wind_spd = block['wind']['speed'] * 3.6 # m/s to km/h
            wind_deg = block['wind']['deg']
            pressure = block['main']['pressure']
            
            # Encode precip type: 1 if rain or snow, 0 otherwise
            precip_type = 1.0 if 'rain' in block or 'snow' in block else 0.0
            
            lstm_sequence[hour] = [temp, hum, wind_spd, wind_deg, pressure, precip_type]


        return {
            "temperature": current_temp,
            "humidity": current_humidity,
            "current_rainfall": current_rainfall,
            "annual_rainfall": 1050.0, # Generally static or fetched from climate DB, mocking for real-time
            "weather_sequence_7_days": lstm_sequence,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"OpenWeatherMap API Error: {e}")
        return _get_fallback_weather_data()
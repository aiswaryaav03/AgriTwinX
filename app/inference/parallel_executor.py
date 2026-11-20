import logging
import concurrent.futures
from typing import Dict, Any
import numpy as np

# Import the inference functions from the AI Core wrappers
from app.ai_core.disease_model import predict_disease
from app.ai_core.pest_model import predict_pest
from app.ai_core.nutrient_irrigation_model import predict_nutrient_and_irrigation
from app.ai_core.yield_model import predict_yield
from app.ai_core.weather_risk_model import predict_weather_risk

logger = logging.getLogger(__name__)

def run_parallel_inference(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes all 5 AI models concurrently using a ThreadPool.
    Expects a pre-validated dictionary containing all necessary features.
    Catches individual model failures to ensure the dashboard still loads partial results.
    """
    results = {}
    
    # We use 5 workers because we have exactly 5 independent models to run
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        # 1. Dispatch Disease Prediction
        # Requires: image_path, variety_encoded, age_scaled
        disease_future = executor.submit(
            predict_disease,
            image_path=input_data.get('image_path', ''),
            variety_encoded=input_data.get('variety_encoded', 0),
            age_scaled=input_data.get('age_scaled', 0.0)
        )
        
        # 2. Dispatch Pest Detection
        # Requires: image_path
        pest_future = executor.submit(
            predict_pest,
            image_path=input_data.get('image_path', '')
        )
        
        # 3. Dispatch Nutrient & Irrigation Prediction
        # Requires: temp, humidity, ph, rainfall, current_n, current_p, current_k
        nutrient_irr_future = executor.submit(
            predict_nutrient_and_irrigation,
            temp=input_data.get('temperature', 25.0),
            humidity=input_data.get('humidity', 70.0),
            ph=input_data.get('soil_pH', 6.5),
            rainfall=input_data.get('current_rainfall', 0.0),
            current_n=input_data.get('soil_N', 0.0),
            current_p=input_data.get('soil_P', 0.0),
            current_k=input_data.get('soil_K', 0.0)
        )
        
        # 4. Dispatch Yield Prediction
        # Requires: season, state, area_acres, annual_rainfall, fertilizer_kg, pesticide_kg
        yield_future = executor.submit(
            predict_yield,
            season=input_data.get('season', 'Kharif'),
            state=input_data.get('state', 'Tamil Nadu'),
            area_acres=input_data.get('farm_size', 1.0),
            annual_rainfall=input_data.get('annual_rainfall', 1000.0),
            fertilizer_kg=input_data.get('fertilizer_used', 0.0),
            pesticide_kg=input_data.get('pesticide_used', 0.0)
        )
        
        # 5. Dispatch Weather Risk (LSTM) Prediction
        # Requires: 168-hour (7 day) numpy array sequence
        # We provide a safe fallback of zeros if the weather API failed to provide the sequence
        default_weather_seq = np.zeros((168, 6)) 
        weather_future = executor.submit(
            predict_weather_risk,
            weather_sequence_7_days=input_data.get('weather_sequence_7_days', default_weather_seq)
        )

        
        # Collect Disease Results
        try:
            results['disease_analysis'] = disease_future.result(timeout=15)
        except Exception as e:
            logger.error(f"Disease Model Timeout/Error: {e}")
            results['disease_analysis'] = {"error": str(e)}

        # Collect Pest Results
        try:
            results['pest_analysis'] = pest_future.result(timeout=15)
        except Exception as e:
            logger.error(f"Pest Model Timeout/Error: {e}")
            results['pest_analysis'] = {"error": str(e)}

        # Collect Nutrient & Irrigation Results
        try:
            results['nutrient_irrigation_analysis'] = nutrient_irr_future.result(timeout=10)
        except Exception as e:
            logger.error(f"Nutrient/Irrigation Model Timeout/Error: {e}")
            results['nutrient_irrigation_analysis'] = {"error": str(e)}

        # Collect Yield Results
        try:
            results['yield_analysis'] = yield_future.result(timeout=5)
        except Exception as e:
            logger.error(f"Yield Model Timeout/Error: {e}")
            results['yield_analysis'] = {"error": str(e)}

        # Collect Weather Risk Results
        try:
            results['weather_risk_analysis'] = weather_future.result(timeout=10)
        except Exception as e:
            logger.error(f"Weather Risk Model Timeout/Error: {e}")
            results['weather_risk_analysis'] = {"error": str(e)}

    return results
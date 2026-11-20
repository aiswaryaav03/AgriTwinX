import shap
import numpy as np
import pandas as pd
import logging
from app.ai_core import registry

logger = logging.getLogger(__name__)

def generate_yield_shap(season_encoded: int, state_encoded: int, area_ha: float, 
                        annual_rainfall: float, fertilizer_kg: float, pesticide_kg: float) -> list:
    """
    Generates SHAP feature importance percentages for the LightGBM yield prediction.
    Returns a sorted list of dictionaries suitable for the frontend Waterfall Chart.
    """
    model = registry.models.get('yield')
    if model is None:
        return []

    try:
        # Create the feature dataframe matching the training setup exactly
        features = ['Season', 'State', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
        input_data = pd.DataFrame([{
            'Season': season_encoded,
            'State': state_encoded,
            'Area': area_ha,
            'Annual_Rainfall': annual_rainfall,
            'Fertilizer': fertilizer_kg,
            'Pesticide': pesticide_kg
        }])

        # Initialize TreeExplainer (Fast for LightGBM)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_data)[0] # Extract values for the single instance

        # Calculate absolute impact to determine percentage contribution
        abs_shap = np.abs(shap_values)
        total_impact = np.sum(abs_shap)
        
        # Avoid division by zero
        if total_impact == 0:
            total_impact = 1e-9

        # Map features to readable names for the UI
        feature_mapping = {
            'Season': 'Crop Season',
            'State': 'Region/State',
            'Area': 'Farm Area',
            'Annual_Rainfall': 'Annual Rainfall',
            'Fertilizer': 'Fertilizer Input',
            'Pesticide': 'Pesticide Input'
        }

        impact_results = []
        for i, feature in enumerate(features):
            percentage = (abs_shap[i] / total_impact) * 100
            impact_results.append({
                "feature": feature_mapping.get(feature, feature),
                "impact_percentage": round(percentage, 1),
                "raw_shap_value": round(float(shap_values[i]), 3),
                # If SHAP is positive, it pushed the yield up. If negative, it pulled it down.
                "direction": "positive" if shap_values[i] > 0 else "negative"
            })

        # Sort by impact percentage (highest first)
        impact_results = sorted(impact_results, key=lambda x: x['impact_percentage'], reverse=True)
        return impact_results

    except Exception as e:
        logger.error(f"Error generating Yield SHAP: {e}")
        return []


def generate_irrigation_shap(temp: float, humidity: float, ph: float, 
                             n: float, p: float, k: float) -> list:
    """
    Generates SHAP feature importance for the XGBoost Irrigation prediction.
    Returns a sorted list of dictionaries suitable for the frontend Horizontal Bar Chart.
    """
    irr_model = registry.models.get('irrigation')
    scalers = registry.models.get('scalers', {}).get('nutrient')
    
    if irr_model is None or scalers is None:
        return []

    try:
        scaler_irr_X = scalers['scaler_irr_X']
        
        # Raw input array
        irr_input = np.array([[temp, humidity, ph, n, p, k]])
        # Model expects scaled data
        irr_input_scaled = scaler_irr_X.transform(irr_input)

        explainer = shap.TreeExplainer(irr_model)
        shap_values = explainer.shap_values(irr_input_scaled)[0]

        abs_shap = np.abs(shap_values)
        total_impact = np.sum(abs_shap)
        if total_impact == 0:
            total_impact = 1e-9

        features = ['Temperature', 'Humidity', 'Soil pH', 'Soil Nitrogen', 'Soil Phosphorus', 'Soil Potassium']
        
        impact_results = []
        for i, feature in enumerate(features):
            percentage = (abs_shap[i] / total_impact) * 100
            impact_results.append({
                "feature": feature,
                "impact_percentage": round(percentage, 1),
                "direction": "positive" if shap_values[i] > 0 else "negative"
            })

        return sorted(impact_results, key=lambda x: x['impact_percentage'], reverse=True)

    except Exception as e:
        logger.error(f"Error generating Irrigation SHAP: {e}")
        return []
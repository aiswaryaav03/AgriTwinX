import numpy as np
from . import registry

def predict_nutrient_and_irrigation(temp: float, humidity: float, ph: float, 
                                    rainfall: float, current_n: float, 
                                    current_p: float, current_k: float) -> dict:
    """
    Uses the Phase 1.3 dual XGBoost pipeline.
    1. Predicts IDEAL N, P, K given the environment. Compares it to current values to find deficiency.
    2. Predicts IDEAL irrigation (rainfall equivalent in mm) given current soil and environment.
    """
    nut_models = registry.models.get('nutrient') # Dict of {'N': model, 'P': model, 'K': model}
    irr_model = registry.models.get('irrigation')
    scalers = registry.models.get('scalers', {}).get('nutrient')
    
    if nut_models is None or irr_model is None or scalers is None:
        return {
            "nutrient_status": "Unknown (Models Not Loaded)",
            "irrigation_requirement": 0.0
        }

    try:
        scaler_nut_X = scalers['scaler_nut_X']
        scaler_nut_y = scalers['scaler_nut_y']
        scaler_irr_X = scalers['scaler_irr_X']
        scaler_irr_y = scalers['scaler_irr_y']

        # 1. Nutrient Prediction (What SHOULD the soil have?)
        # Features: ['temperature', 'humidity', 'ph', 'rainfall']
        nut_input = np.array([[temp, humidity, ph, rainfall]])
        nut_input_scaled = scaler_nut_X.transform(nut_input)
        
        pred_N = nut_models['N'].predict(nut_input_scaled)[0]
        pred_P = nut_models['P'].predict(nut_input_scaled)[0]
        pred_K = nut_models['K'].predict(nut_input_scaled)[0]
        
        # Inverse transform to get actual ideal values
        ideal_npk_scaled = np.array([[pred_N, pred_P, pred_K]])
        ideal_npk = scaler_nut_y.inverse_transform(ideal_npk_scaled)[0]
        
        ideal_n, ideal_p, ideal_k = ideal_npk[0], ideal_npk[1], ideal_npk[2]
        
        # Determine Deficiency Logic
        deficiency = []
        if current_n < ideal_n * 0.8: deficiency.append("Nitrogen")
        if current_p < ideal_p * 0.8: deficiency.append("Phosphorus")
        if current_k < ideal_k * 0.8: deficiency.append("Potassium")
        
        if not deficiency:
            status = "Optimal Nutrient Levels"
        else:
            status = f"{', '.join(deficiency)} Deficiency"

        # 2. Irrigation Prediction
        # Features: ['temperature', 'humidity', 'ph', 'N', 'P', 'K']
        irr_input = np.array([[temp, humidity, ph, current_n, current_p, current_k]])
        irr_input_scaled = scaler_irr_X.transform(irr_input)
        
        pred_irr_scaled = irr_model.predict(irr_input_scaled)
        ideal_rainfall = scaler_irr_y.inverse_transform(pred_irr_scaled.reshape(-1, 1))[0][0]
        
        # If it's already raining more than needed, irrigation is 0
        irrigation_needed = max(0.0, ideal_rainfall - rainfall)

        return {
            "nutrient_status": str(status),
            "ideal_n": float(np.round(ideal_n, 1)),
            "ideal_p": float(np.round(ideal_p, 1)),
            "ideal_k": float(np.round(ideal_k, 1)),
            "irrigation_requirement": float(np.round(irrigation_needed, 2))
        }
        
    except Exception as e:
        return {"error": str(e)}
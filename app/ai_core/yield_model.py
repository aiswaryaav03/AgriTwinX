import numpy as np
import pandas as pd
from . import registry

def predict_yield(season: str, state: str, area_acres: float, 
                  annual_rainfall: float, fertilizer_kg: float, 
                  pesticide_kg: float) -> float:
    """
    Uses the Phase 1.4 LightGBM model to predict Yield in tons per hectare.
    Profit calculations are decoupled and handled in the Financial Service later.
    """
    model = registry.models.get('yield')
    encoders = registry.models.get('encoders', {}).get('yield')
    
    if model is None or encoders is None:
        return 0.0

    try:
        # Encode categoricals using the saved LabelEncoders
        # Use safe defaults if the exact state/season isn't in the training data
        season_encoded = encoders['Season'].transform([season])[0] if season in encoders['Season'].classes_ else 0
        state_encoded = encoders['State'].transform([state])[0] if state in encoders['State'].classes_ else 0
        
        # Convert Area from Acres to Hectares as the model was trained on Hectares
        area_hectares = area_acres * 0.404686
        
        # Feature order must match training exactly:
        # ['Season', 'State', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
        features = pd.DataFrame([{
            'Season': season_encoded,
            'State': state_encoded,
            'Area': area_hectares,
            'Annual_Rainfall': annual_rainfall,
            'Fertilizer': fertilizer_kg,
            'Pesticide': pesticide_kg
        }])
        
        pred_yield = model.predict(features)[0]
        
        # Prevent negative predictions in extreme edge cases
        return max(0.0, round(float(pred_yield), 2))
        
    except Exception as e:
        print(f"Yield Prediction Error: {e}")
        return 0.0
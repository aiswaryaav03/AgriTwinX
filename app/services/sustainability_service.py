import logging

logger = logging.getLogger(__name__)

def calculate_sustainability_score(farm_size_acres: float, fertilizer_kg: float, pesticide_kg: float, irrigation_mm_day: float) -> dict:
    """
    Calculates a 0-100 sustainability score based on farm inputs and AI-predicted irrigation needs.
    Returns the score along with UI-ready text for the Sustainability Card.
    """
    try:
        # Prevent division by zero
        if farm_size_acres <= 0:
            farm_size_acres = 1.0
            
        # Calculate per-acre metrics
        fert_per_acre = fertilizer_kg / farm_size_acres
        pest_per_acre = pesticide_kg / farm_size_acres
        
        # Start with a perfect score and deduct based on penalties
        score = 100
        
        # 1. Water Efficiency Evaluation
        if irrigation_mm_day > 10.0:
            score -= 15
            water_eff = f"Poor - {irrigation_mm_day:.1f} mm/day average, high consumption."
        elif irrigation_mm_day > 4.0:
            score -= 5
            water_eff = f"Good - {irrigation_mm_day:.1f} mm/day average, within optimal range."
        else:
            water_eff = f"Excellent - {irrigation_mm_day:.1f} mm/day average, highly efficient."
            
        # 2. Chemical Usage (Pesticide) Evaluation
        if pest_per_acre > 1.0:
            score -= 20
            chem_usage = "High - Excessive pesticide application."
            suggestion = "Reduce pesticide reliance. Adopt Integrated Pest Management (IPM) to improve score."
        elif pest_per_acre > 0.4:
            score -= 10
            chem_usage = "Moderate - Average pesticide application."
            suggestion = "Switch to neem oil for next application to improve your score by 8 points."
        else:
            chem_usage = "Low - Excellent chemical management."
            suggestion = "Keep up the organic and sustainable practices!"
            
        # 3. Fertilizer Penalty (Excessive nitrogen runoff risk)
        if fert_per_acre > 40:
            score -= 10
            
        # Clamp score between 0 and 100
        score = max(0, min(100, int(score)))
        
        return {
            "score": score,
            "water_efficiency": water_eff,
            "chemical_usage": chem_usage,
            "suggestion": suggestion
        }
        
    except Exception as e:
        logger.error(f"Error calculating sustainability score: {e}")
        return {
            "score": 50,
            "water_efficiency": "Unknown",
            "chemical_usage": "Unknown",
            "suggestion": "Data insufficient for sustainability analysis."
        }
import os
import json
import logging
from flask import current_app
from groq import Groq

logger = logging.getLogger(__name__)


def _get_groq_client():
    """Initializes the Groq client securely using the app config."""
    api_key = current_app.config.get('GROQ_API_KEY')
    if not api_key or api_key == 'your_groq_api_key_here':
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {e}")
        return None

def _get_fallback_calendar() -> dict:
    """Fallback static calendar if LLM fails."""
    return {
        "Week 1 - Day 1 to 7": "Monitor crop health daily. Irrigate if topsoil is dry. Follow basic NPK guidelines based on soil test.",
        "Week 2 - Day 8 to 14": "Check for early signs of pests. Apply preventive measures if regional risk is high.",
        "Week 3 - Day 15 to 21": "Maintain optimal water levels. Continue monitoring for disease symptoms."
    }

def _get_fallback_treatment(options: list) -> dict:
    """Fallback static treatment comparison if LLM fails."""
    fallback = {}
    for opt in options:
        fallback[f"Option - {opt}"] = "Analysis unavailable at this time due to API timeout. Please consult local agronomist."
    return fallback


def generate_farming_calendar(model_results: dict) -> dict:
    """
    Uses LLaMA 3 to generate a week-by-week prescriptive farming schedule
    based on the aggregated outputs of all 5 AI models.
    """
    client = _get_groq_client()
    if not client:
        return _get_fallback_calendar()

    # Construct the context prompt from model outputs
    disease = model_results.get('disease_analysis', {}).get('disease', 'None')
    pest = model_results.get('pest_analysis', {}).get('pest', 'None')
    nutrients = model_results.get('nutrient_irrigation_analysis', {}).get('nutrient_status', 'Optimal')
    irrigation = model_results.get('nutrient_irrigation_analysis', {}).get('irrigation_requirement', 0)
    weather_risk = model_results.get('weather_risk_analysis', {}).get('risk_level', 'Low')
    
    prompt = f"""
    You are an expert precision agriculture agronomist specializing in paddy farming.
    Based on the following AI Digital Twin analysis, generate a strict 3-week actionable farming calendar.
    
    Current Status:
    - Disease Detected: {disease}
    - Pest Detected: {pest}
    - Nutrient Status: {nutrients}
    - Irrigation Need: {irrigation} mm/day
    - 7-Day Weather Risk: {weather_risk}
    
    Output strictly as a JSON object with exactly three keys:
    "Week 1 - Day 1 to 7", "Week 2 - Day 8 to 14", "Week 3 - Day 15 to 21".
    The value for each key must be a concise, action-oriented string.
    Do not include markdown blocks, only the raw JSON.
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        return json.loads(result_content)
        
    except Exception as e:
        logger.error(f"Groq API Error (Calendar): {e}")
        return _get_fallback_calendar()


def simulate_treatment(disease: str, severity: str, age: int, stage: str, weather_summary: str, size: float, options: list) -> dict:
    """
    Uses LLaMA 3 to compare farmer-selected treatment options for a specific disease.
    Generates cost, efficacy, and safety comparisons.
    """
    client = _get_groq_client()
    if not client:
        return _get_fallback_treatment(options)
        
    options_str = ", ".join(options)
    
    prompt = f"""
    You are an expert agronomist providing a comparative treatment analysis for a paddy farmer.
    
    Farm Context:
    - Disease: {disease} (Severity: {severity})
    - Crop Age: {age} days (Stage: {stage})
    - Weather: {weather_summary}
    - Farm Size: {size} acres
    
    The farmer is considering these options: {options_str}
    
    Compare each option based on Yield Recovery, Cost, Speed of Recovery, and Environmental Safety.
    Output strictly as a JSON object where the keys are the exact option names provided.
    The value for each key must be a concise string summarizing the pros/cons and financial impact.
    Do not include markdown blocks, only the raw JSON.
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.4,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        return json.loads(result_content)
        
    except Exception as e:
        logger.error(f"Groq API Error (Treatment): {e}")
        return _get_fallback_treatment(options)
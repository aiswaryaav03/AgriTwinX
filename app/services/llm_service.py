import logging
from typing import List
from app.integrations.groq_api import generate_farming_calendar, simulate_treatment

logger = logging.getLogger(__name__)

def get_farming_calendar(ai_results: dict) -> dict:
    """
    Service wrapper for generating the 3-week farming calendar.
    Passes the aggregated AI inference results to the Groq LLaMA 3 integration.
    """
    logger.info("Requesting Farming Calendar from LLM...")
    return generate_farming_calendar(ai_results)

def get_treatment_comparison(disease: str, severity: str, age: int, stage: str, 
                             weather_summary: str, size: float, options: List[str]) -> dict:
    """
    Service wrapper for the Treatment Simulator.
    Passes the contextual farm data and user-selected options to the Groq LLM.
    """
    logger.info(f"Requesting Treatment Simulation for {disease} with options: {options}")
    return simulate_treatment(disease, severity, age, stage, weather_summary, size, options)
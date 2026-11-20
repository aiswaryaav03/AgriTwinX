import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.database.db_setup import db
from app.models.field_input import FieldInput
from app.models.prediction import Prediction
from app.models.farming_calendar import FarmingCalendar
from app.models.treatment_log import TreatmentLog


# Import orchestrators and services
from app.inference.parallel_executor import run_parallel_inference
from app.xai_core.gradcam_generator import generate_disease_heatmap
from app.xai_core.shap_generator import generate_yield_shap, generate_irrigation_shap
from app.services.sustainability_service import calculate_sustainability_score
from app.services.financial_service import calculate_financials
from app.services.llm_service import get_farming_calendar, get_treatment_comparison
from app.integrations.openweather_api import fetch_weather_data
from app.services.weather_forecast_service import generate_daily_forecast

# Import utilities
from app.utils.file_handler import save_uploaded_image
from app.utils.regional_defaults import get_soil_defaults

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_field():
    """
    The Core Engine of AgriTwinX. 
    Handles the multipart form data, saves the image, orchestrates the 5 parallel AI models,
    generates XAI heatmaps, requests the LLM calendar, and saves everything to the DB.
    """
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Leaf image is required."}), 400
            
        file = request.files['image']
        # Save image securely and get absolute path for OpenCV and relative path for UI
        abs_img_path, rel_img_path = save_uploaded_image(file, current_app.config['UPLOAD_FOLDER'])
        
        if not abs_img_path:
            return jsonify({"error": "Invalid image format."}), 400

        # Parse textual/numerical form data
        crop_age = request.form.get('crop_age', type=int, default=45)
        variety = request.form.get('variety', default='IR-64')
        growth_stage = request.form.get('growth_stage', default='Tillering')
        farm_size = request.form.get('farm_size', type=float, default=current_user.farm_size)
        location = request.form.get('location', default=current_user.village)
        season = request.form.get('season', default='Kharif')
        fert_used = request.form.get('fertilizer_used', type=float, default=0.0)
        pest_used = request.form.get('pesticide_used', type=float, default=0.0)
        
        # Handle Soil Data Fallback (if user chose "Use Regional Average")
        soil_N = request.form.get('soil_N', type=float)
        soil_P = request.form.get('soil_P', type=float)
        soil_K = request.form.get('soil_K', type=float)
        soil_pH = request.form.get('soil_pH', type=float)
        
        if soil_N is None or soil_P is None or soil_K is None or soil_pH is None:
            defaults = get_soil_defaults(location)
            soil_N, soil_P, soil_K, soil_pH = defaults['N'], defaults['P'], defaults['K'], defaults['pH']

        weather_data = fetch_weather_data(location)

        # Build massive structured input dict for the parallel executor
        input_data = {
            "image_path": abs_img_path,
            # Variety encoding placeholder logic (In production, map to LabelEncoder integer)
            "variety_encoded": 1 if variety == 'IR-64' else 0, 
            # Age scaling placeholder logic (In production, map to StandardScaler logic)
            "age_scaled": (crop_age - 45.0) / 10.0, 
            "temperature": weather_data['temperature'],
            "humidity": weather_data['humidity'],
            "current_rainfall": weather_data['current_rainfall'],
            "annual_rainfall": weather_data['annual_rainfall'],
            "weather_sequence_7_days": weather_data['weather_sequence_7_days'],
            "soil_N": soil_N,
            "soil_P": soil_P,
            "soil_K": soil_K,
            "soil_pH": soil_pH,
            "season": season,
            "state": "Tamil Nadu", # Extracted natively from location string in real prod
            "farm_size": farm_size,
            "fertilizer_used": fert_used,
            "pesticide_used": pest_used
        }

        ai_results = run_parallel_inference(input_data)

        heatmap_rel_path = ""
        disease_res = ai_results.get('disease_analysis', {})
        if 'class_idx' in disease_res and not disease_res.get('error'):
            heatmap_rel_path = generate_disease_heatmap(
                image_path=abs_img_path, 
                variety_encoded=input_data['variety_encoded'], 
                age_scaled=input_data['age_scaled'], 
                predicted_class_idx=disease_res['class_idx']
            )
            
        # SHAP for XGBoost and LightGBM
        yield_res = ai_results.get('yield_analysis', 0.0)
        yield_shap = generate_yield_shap(
            input_data['variety_encoded'], input_data['variety_encoded'], farm_size, 
            input_data['annual_rainfall'], fert_used, pest_used
        )
        
        irrigation_shap = generate_irrigation_shap(
            input_data['temperature'], input_data['humidity'], soil_pH, 
            soil_N, soil_P, soil_K
        )

        sustainability = calculate_sustainability_score(
            farm_size, fert_used, pest_used, 
            ai_results.get('nutrient_irrigation_analysis', {}).get('irrigation_requirement', 0.0)
        )
        
        financials = calculate_financials(yield_res, farm_size, fert_used, pest_used)

        calendar_json = get_farming_calendar(ai_results)

        # Store Inputs
        field_input = FieldInput(
            user_id=current_user.id, crop_age=crop_age, variety=variety, growth_stage=growth_stage,
            soil_N=soil_N, soil_P=soil_P, soil_K=soil_K, 
            soil_pH=soil_pH, fertilizer_used=fert_used, 
            pesticide_used=pest_used
        )
        db.session.add(field_input)
        db.session.flush() # Flush to get field_input.id

        overall_weather = ai_results.get("weather_risk_analysis", {})

        weather_payload = generate_daily_forecast(
            input_data["weather_sequence_7_days"],
            overall_weather
        )
        prediction = Prediction(
            user_id=current_user.id, input_id=field_input.id,
            disease_label=disease_res.get('disease'), confidence=disease_res.get('confidence'),
            nutrient_status=ai_results.get('nutrient_irrigation_analysis', {}).get('nutrient_status'),
            pest_type=ai_results.get('pest_analysis', {}).get('pest'),
            pest_risk_score=ai_results.get('pest_analysis', {}).get('risk_score'),
            irrigation_requirement=ai_results.get('nutrient_irrigation_analysis', {}).get('irrigation_requirement'),
            yield_forecast=financials.get('predicted_yield_t_ha'),
            expected_profit=financials.get('expected_profit_inr'),
            sustainability_score=sustainability.get('score'),
            heatmap_path=heatmap_rel_path,
            weather_impact_json=weather_payload
        )
        db.session.add(prediction)

        # Store Calendar
        db_calendar = FarmingCalendar(
            user_id=current_user.id, week_number=1, schedule_json=calendar_json
        )
        db.session.add(db_calendar)
        print(weather_payload)
        db.session.commit()

        response_payload = {
            "status": "success",
            "images": {
                "original": rel_img_path,
                "heatmap": heatmap_rel_path,
                "pest_bbox": ai_results.get('pest_analysis', {}).get('bbox')
            },
            "disease": disease_res,
            "pest": ai_results.get('pest_analysis'),
            "soil_water": ai_results.get('nutrient_irrigation_analysis'),
            "financials": financials,
            "weather": weather_payload,
            "sustainability": sustainability,
            "calendar": calendar_json,
            "xai": {
                "yield_shap": yield_shap,
                "irrigation_shap": irrigation_shap
            }
        }
        
        return jsonify(response_payload), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"API Error during analysis: {str(e)}")
        return jsonify({"error": f"An internal system error occurred: {str(e)}"}), 500


@api_bp.route('/treatment/compare', methods=['POST'])
@login_required
def compare_treatment():
    """
    LLM-powered Treatment Simulator endpoint.
    Takes user options and farm context, returns a LLaMA 3 comparative analysis.
    """
    data = request.json
    if not data or 'options' not in data:
        return jsonify({"error": "Treatment options are required."}), 400
        
    disease = data.get('disease', 'Unknown')
    severity = data.get('severity', 'Moderate')
    age = data.get('crop_age', 45)
    stage = data.get('growth_stage', 'Tillering')
    weather_summary = data.get('weather_summary', 'Clear skies, 30C')
    size = current_user.farm_size
    options = data.get('options', [])
    
    # Request Groq LLaMA 3 Analysis
    comparison_results = get_treatment_comparison(
        disease, severity, age, stage, weather_summary, size, options
    )
    
    # Log the interaction for system learning
    options_str = " vs ".join(options)
    log = TreatmentLog(
        user_id=current_user.id, disease=disease, 
        treatment_chosen=options_str, groq_response_json=comparison_results
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "comparison": comparison_results
    }), 200
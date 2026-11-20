from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.prediction import Prediction
from app.models.field_input import FieldInput
from app.models.treatment_log import TreatmentLog
from app.models.farming_calendar import FarmingCalendar
from flask import render_template
from flask_login import login_required

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the main farmer dashboard. 
    Fetches the latest prediction to populate the UI cards.
    """
    # Fetch the most recent prediction and its associated inputs for the current user
    latest_prediction = Prediction.query.filter_by(user_id=current_user.id)\
                                        .order_by(Prediction.created_at.desc())\
                                        .first()
                                        
    latest_calendar = FarmingCalendar.query.filter_by(user_id=current_user.id)\
                                           .order_by(FarmingCalendar.groq_generated_at.desc())\
                                           .first()

    return render_template(
        'farmer/dashboard.html', 
        user=current_user,
        prediction=latest_prediction,
        calendar=latest_calendar,
    )
@farmer_bp.route("/analyse")
@login_required
def analyse():
    return render_template(
        "farmer/analyse.html",
        user=current_user
    )

@farmer_bp.route('/history')
@login_required
def history():
    """
    Renders a timeline of all past field analyses.
    """
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
                                  .order_by(Prediction.created_at.desc())\
                                  .all()
    return render_template('farmer/history.html', user=current_user, history=predictions)

@farmer_bp.route('/treatment-simulator')
@login_required
def treatment_simulator():
    """
    Renders the What-If simulation interface for disease treatments.
    """
    latest_prediction = Prediction.query.filter_by(user_id=current_user.id)\
                                        .order_by(Prediction.created_at.desc())\
                                        .first()
    
    past_logs = TreatmentLog.query.filter_by(user_id=current_user.id)\
                                  .order_by(TreatmentLog.action_date.desc())\
                                  .all()
                                  
    return render_template(
        'farmer/treatment.html', 
        user=current_user, 
        prediction=latest_prediction,
        logs=past_logs
    )

@farmer_bp.route('/weather-impact')
@login_required
def weather_impact():
    """
    Renders the 7-day LSTM weather risk view for the farmer's latest analysis.
    """
    latest_prediction = Prediction.query.filter_by(user_id=current_user.id)\
                                        .order_by(Prediction.created_at.desc())\
                                        .first()

    return render_template(
        'farmer/weather_impact.html',
        user=current_user,
        prediction=latest_prediction
    )

@farmer_bp.route('/calendar')
@login_required
def calendar():
    """
    Renders the full LLaMA 3 generated farming calendar.
    """
    latest_calendar = FarmingCalendar.query.filter_by(user_id=current_user.id)\
                                           .order_by(FarmingCalendar.groq_generated_at.desc())\
                                           .first()

    return render_template(
        'farmer/calendar.html',
        user=current_user,
        calendar=latest_calendar
    )

@farmer_bp.route('/settings')
@login_required
def settings():
    """
    Renders the farmer's read-only account settings/overview page.
    """
    return render_template(
        'farmer/settings.html',
        user=current_user
    )
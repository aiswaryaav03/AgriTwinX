from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from app.middleware.auth_middleware import admin_required
from app.models.user import User
from app.models.prediction import Prediction
from app.models.feedback import Feedback
from app.models.market_price import MarketPrice
from app.database.db_setup import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """
    Renders the master admin control panel.
    Displays aggregate metrics across all farmers.
    """
    total_users = User.query.count() - 1 # Exclude the admin user itself
    total_analyses = Prediction.query.count()
    feedbacks = Feedback.query.order_by(Feedback.harvest_date.desc()).all()
    
    # Fetch current global market prices
    market_prices = MarketPrice.query.all()
    
    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_analyses=total_analyses,
        feedbacks=feedbacks,
        market_prices=market_prices
    )

@admin_bp.route('/update-price', methods=['POST'])
@login_required
@admin_required
def update_price():
    """
    Allows the admin to dynamically update the global crop market price.
    This directly affects the LightGBM yield profit calculation for all future farmer predictions.
    """
    crop = request.form.get('crop_name', 'Rice')
    new_price = request.form.get('price_per_ton', type=float)
    
    if new_price and new_price > 0:
        price_record = MarketPrice.query.filter_by(crop_name=crop).first()
        if not price_record:
            price_record = MarketPrice(crop_name=crop, price_per_ton=new_price)
            db.session.add(price_record)
        else:
            price_record.price_per_ton = new_price
            
        try:
            db.session.commit()
            flash(f'Market price for {crop} updated to ₹{new_price}/ton.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Database error while updating price.', 'error')
    else:
        flash('Invalid price entered.', 'warning')
        
    return redirect('/admin')
from flask import Blueprint, render_template, request, redirect, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.database.db_setup import db
from app.utils.security import hash_password, verify_password

# Initialize Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user authentication. 
    Routes to Admin Panel if credentials match the hardcoded admin config.
    Otherwise, routes to the Farmer Dashboard.
    """
    if current_user.is_authenticated:
        # Prevent logged-in users from seeing the login page
        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@agritwinx.com')
        if current_user.email == admin_email:
            return redirect('/admin')
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@agritwinx.com')
        admin_pass = current_app.config.get('ADMIN_PASSWORD', 'Admin@2024')

        # 1. Check for Hardcoded Admin Login
        if email == admin_email and password == admin_pass:
            # We need an admin user object in DB to satisfy Flask-Login session management
            admin_user = User.query.filter_by(email=admin_email).first()
            if not admin_user:
                # Seed the admin user if it doesn't exist
                admin_user = User(
                    name="System Admin", 
                    phone="0000000000", 
                    email=admin_email, 
                    village="System", 
                    farm_size=0, 
                    password_hash=hash_password(admin_pass)
                )
                db.session.add(admin_user)
                db.session.commit()
            
            login_user(admin_user)
            return redirect('/admin')

        # 2. Check for Farmer Login
        user = User.query.filter_by(email=email).first()
        if user and verify_password(user.password_hash, password):
            login_user(user)
            # Redirecting to a hardcoded string until dashboard route is generated
            return redirect('/dashboard') 
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles Farmer registration as defined in the Requirement Collection Form.
    """
    if current_user.is_authenticated:
        return redirect('/dashboard')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        village = request.form.get('village', '').strip()
        farm_size = request.form.get('farm_size', type=float)
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect('/signup')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'error')
            return redirect('/login')

        if User.query.filter_by(phone=phone).first():
            flash('Phone number already registered.', 'error')
            return redirect('/signup')

        # Create New Farmer Profile
        new_user = User(
            name=name,
            phone=phone,
            email=email,
            village=village,
            farm_size=farm_size,
            password_hash=hash_password(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            # Log the error in a real production scenario

    return render_template('auth/signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Clears the session and logs the user out."""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect('/login')
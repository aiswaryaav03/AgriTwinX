from functools import wraps
from flask import redirect, url_for, flash, current_app
from flask_login import current_user

def admin_required(f):
    """
    Decorator to restrict access to the Admin panel.
    Checks if the currently logged-in user matches the hardcoded admin credentials.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Admin credentials are meant to be in config, defaulting to standard if missing
        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@agritwinx.com')
        
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
            
        if current_user.email != admin_email:
            flash("Access denied. Admin privileges required.", "error")
            return redirect('/dashboard') # Redirect unauthorized farmers back to their dashboard
            
        return f(*args, **kwargs)
    return decorated_function
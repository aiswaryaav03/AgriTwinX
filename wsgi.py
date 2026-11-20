import os
from app import create_app

# Force the environment to production for WSGI execution
env = os.environ.get('FLASK_ENV', 'production')

# Create the Flask application instance
# This 'app' object is what Gunicorn or uWSGI will interface with
app = create_app(env)

if __name__ == '__main__':
    # This block is typically ignored by Gunicorn, 
    # but serves as a fallback if executed directly
    app.run()
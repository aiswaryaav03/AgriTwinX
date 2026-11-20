import os
import logging
from app import create_app
from app.database.db_setup import db
from app.ai_core import registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = os.environ.get('FLASK_ENV', 'development')

app = create_app(env)
import os

print("=" * 60)
print("Current Working Directory:", os.getcwd())
print("App Root Path:", app.root_path)
print("App Instance Path:", app.instance_path)
print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
print("Database Exists:", os.path.exists(os.path.join(app.instance_path, "agritwinx.db")))
print("=" * 60)

#engine = db.engine
#print("Engine URL:", engine.url)
#print("Engine Database:", engine.url.database)

with app.app_context():
    logger.info("Verifying database tables...")
    import os

    print("Current Working Directory:", os.getcwd())
    print("App Root:", app.root_path)
    print("Instance Path:", app.instance_path)
    print("URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    engine = db.engine
    print("Engine URL:", engine.url)
    print("Engine Database:", engine.url.database)
    print("Absolute Exists:", os.path.exists(os.path.abspath(engine.url.database)))
    db.create_all()
    weights_dir = os.path.join(os.getcwd(), "ai_weights")
    logger.info(f"Loading AI models from: {weights_dir}")
    registry.load_all_models(weights_dir)
    

if __name__ == '__main__':
    logger.info(f"Starting AgriTwinX in {env} mode...")
    
    app.run(host='0.0.0.0', port=5001)
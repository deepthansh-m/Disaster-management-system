# backend/app.py
from flask import Flask
from flask_cors import CORS
from backend.config.database import engine, Base
from backend.routes import register_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.middleware.error_handler import handle_error
import os
from dotenv import load_dotenv
import logging

load_dotenv()
# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "postgresql://postgres:Mani%402003@localhost/disaster_prediction")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configure CORS 
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:1234"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }},
         expose_headers=["Content-Range", "X-Content-Range"])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:1234')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Register routes
    register_routes(app)

    logger.info("Flask app has been created and configured.")

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Create tables
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    
    app.run(debug=True)
from flask import Blueprint
from backend.controllers.disaster_controller import disaster_bp

# Combine all disaster-related routes
def register_disaster_routes(app):
    app.register_blueprint(disaster_bp)

from flask import Blueprint, jsonify, request
from backend.services.openweather_service import get_weather_data
from backend import app  # Import the app object from the backend module

from backend.controllers.weather_controller import weather_bp
def register_prediction_routes(app):
    app.register_blueprint(weather_bp)
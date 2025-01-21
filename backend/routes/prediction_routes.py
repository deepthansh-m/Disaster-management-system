from flask import Blueprint
from backend.ml.models.prediction_controller import prediction_bp

# Combine all prediction-related routes
def register_prediction_routes(app):
    app.register_blueprint(prediction_bp)

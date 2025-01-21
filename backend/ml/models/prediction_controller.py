from flask import Blueprint, request, jsonify
import joblib
import os
import logging
import numpy as np

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

prediction_bp = Blueprint('prediction', __name__, url_prefix='/details')

# Define model directory relative to this file
MODEL_DIR = r'C:\Users\Asus\Desktop\disaster-management-system\backend\ml\models'

def ensure_model_directory():
    """Ensure model directory exists"""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        logger.info(f"Created model directory at {MODEL_DIR}")

def load_models():
    """Load all needed models, scalers, and encoders."""
    try:
        model_path = os.path.join(MODEL_DIR, 'disaster_type_model.pkl')
        deaths_model_path = os.path.join(MODEL_DIR, 'deaths_model.pkl')
        infra_loss_model_path = os.path.join(MODEL_DIR, 'infra_loss_model.pkl')
        scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
        label_encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')

        model = joblib.load(model_path)
        deaths_model = joblib.load(deaths_model_path)
        infra_loss_model = joblib.load(infra_loss_model_path)
        scaler = joblib.load(scaler_path)
        label_encoder = joblib.load(label_encoder_path)
        test_features = np.array([[28.6, 77.2, 25.0, 1013.0, 80.0, 5.0]])
        test_scaled = scaler.transform(test_features)
        test_pred = infra_loss_model.predict(test_scaled)
        logger.info(f"Test infrastructure loss prediction: {test_pred[0]}")

        return model, deaths_model, infra_loss_model, scaler, label_encoder
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        raise

# Load models at startup
disaster_model, deaths_model, infra_loss_model, scaler, label_encoder = load_models()
@prediction_bp.route('/', methods=['GET'])
def predict_disaster_type():
    try:
        # Extract parameters
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        temp = request.args.get('temp', type=float)
        pressure = request.args.get('pressure', type=float)
        humidity = request.args.get('humidity', type=float)
        wind_speed = request.args.get('wind_speed', type=float)

        # Debug log input values
        logger.debug(f"Input features: lat={lat}, lng={lng}, temp={temp}, "
                    f"pressure={pressure}, humidity={humidity}, wind_speed={wind_speed}")

        if None in [lat, lng, temp, pressure, humidity, wind_speed]:
            return jsonify({"error": "Missing required parameters"}), 400

        # Create and scale features
        features = np.array([[lat, lng, temp, pressure, humidity, wind_speed]])
        logger.debug(f"Raw features shape: {features.shape}")
        logger.debug(f"Raw features: {features}")

        scaled_features = scaler.transform(features)
        logger.debug(f"Scaled features: {scaled_features}")

        # Make predictions
        disaster_type = label_encoder.inverse_transform(disaster_model.predict(scaled_features))[0]
        predicted_deaths = int(deaths_model.predict(scaled_features)[0])
        
        # Debug infrastructure loss prediction
        raw_infra_loss = infra_loss_model.predict(scaled_features)[0]
        logger.debug(f"Raw infrastructure loss prediction: {raw_infra_loss}")
        
        # Ensure positive value and proper scaling
        predicted_infra_loss = max(float(raw_infra_loss), 0.0)
        logger.debug(f"Final infrastructure loss prediction: {predicted_infra_loss}")

        # Calculate severity
        severity = calculate_severity(
            disaster_type,
            predicted_deaths,
            predicted_infra_loss
        )

        logger.info(f"Predictions: type={disaster_type}, deaths={predicted_deaths}, "
                   f"infra_loss={predicted_infra_loss}, severity={severity}")

        return jsonify({
            "status": "success",
            "disaster_type": disaster_type,
            "predicted_deaths": max(predicted_deaths, 0),
            "predicted_infra_loss": predicted_infra_loss,
            "severity": severity
        }), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def calculate_severity(disaster_type, deaths, infra_loss):
    """
    Calculate severity score (0-1) based on multiple factors
    """
    try:
        # Disaster type weights (adjust based on historical data)
        disaster_weights = {
            'Earthquake': 0.9,
            'Flood': 0.7,
            'Cyclone': 0.8,
            'Drought': 0.5,
            'Landslide': 0.6,
            'default': 0.5
        }

        # Get disaster weight (default if type unknown)
        disaster_weight = disaster_weights.get(disaster_type, disaster_weights['default'])

        # Normalize deaths (assume max historical deaths of 10000)
        death_impact = min(deaths / 10000, 1.0)

        # Normalize infrastructure loss (assume max historical loss of $1B)
        infra_impact = min(infra_loss / 1000000000, 1.0)

        # Calculate weighted severity score
        severity = (
            0.4 * death_impact +          # 40% weight to deaths
            0.3 * infra_impact +          # 30% weight to infrastructure
            0.3 * disaster_weight         # 30% weight to disaster type
        )

        return min(max(severity, 0.0), 1.0)  # Ensure between 0 and 1

    except Exception as e:
        logger.error(f"Error calculating severity: {str(e)}")
        return 0.5  # Return medium severity on error
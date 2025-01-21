# backend/ml/models/disaster_predictor.py

import joblib
import pandas as pd

class DisasterPredictor:
    def __init__(self):
        self.disaster_type_model = joblib.load('models/disaster_type_model.pkl')
        self.deaths_model = joblib.load('models/deaths_model.pkl')
        self.infra_loss_model = joblib.load('models/infra_loss_model.pkl')
        self.label_encoder = joblib.load('models/label_encoder.pkl')
        self.disaster_type_mapping = {v: k for k, v in joblib.load('models/disaster_type_mapping.pkl').items()}

    def predict(self, latitude, longitude, parameters):
        temperature = parameters.get('temperature')
        rainfall = parameters.get('rainfall')

        features = pd.DataFrame([[
            float(latitude),
            float(longitude),
            float(temperature),
            float(rainfall)
        ]], columns=['latitude', 'longitude', 'temperature_celsius', 'precip_mm'])

        # Disaster type prediction
        type_pred_code = self.disaster_type_model.predict(features)[0]
        type_confidence = max(self.disaster_type_model.predict_proba(features)[0])
        disaster_type = self.label_encoder.inverse_transform([type_pred_code])[0]

        # Deaths prediction
        deaths_pred = abs(self.deaths_model.predict(features)[0])  # Use abs to avoid negative predictions

        # Infrastructure loss prediction
        infra_loss_pred = abs(self.infra_loss_model.predict(features)[0])

        return {
            "disaster_type": disaster_type,
            "type_confidence": type_confidence,
            "possible_deaths": deaths_pred,
            "infrastructure_loss": infra_loss_pred,
            "parameters": parameters
        }
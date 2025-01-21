import joblib
import numpy as np

# Load models and encoder
disaster_type_model = joblib.load(r'C:\Users\Asus\Desktop\disaster-management-system\models\disaster_type_model.pkl')
label_encoder = joblib.load(r'C:\Users\Asus\Desktop\disaster-management-system\models\label_encoder.pkl')

# Sample input
latitude = 12.97
longitude = 77.59
temperature_celsius = 35.0
precip_mm = 5.0

input_features = np.array([[latitude, longitude, temperature_celsius, precip_mm]])

# Make prediction
disaster_type_code = disaster_type_model.predict(input_features)
disaster_type = label_encoder.inverse_transform(disaster_type_code)

print(f"Predicted Disaster Type: {disaster_type[0]}")
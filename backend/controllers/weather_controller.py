from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

weather_bp = Blueprint('weather', __name__, url_prefix='/map')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not OPENWEATHER_API_KEY:
    raise ValueError("OpenWeather API key not found in environment variables")

@weather_bp.route('/', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
        
    try:
        # Query OpenWeather /weather endpoint in metric units
        url = (
            f'https://api.openweathermap.org/data/2.5/weather'
            f'?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}'
        )
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve weather data"}), response.status_code

        data = response.json()

        # Extract relevant fields, using defaults for missing keys
        temperature_celsius = data.get('main', {}).get('temp', None)
        pressure_hpa = data.get('main', {}).get('pressure', 1013)
        humidity_percent = data.get('main', {}).get('humidity', 50)
        # OpenWeather includes "sea_level" only if available, so fall back
        sea_level_pressure = data.get('main', {}).get('sea_level', pressure_hpa)
        wind_speed_ms = data.get('wind', {}).get('speed', 0)

        return jsonify({
            "temperatureCelsius": temperature_celsius,
            "pressure_hpa": pressure_hpa,
            "humidity_percent": humidity_percent,
            "sea_level_pressure": sea_level_pressure,
            "wind_speed_ms": wind_speed_ms
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
import requests
import os

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather_data(location):
    """Fetch current weather data from OpenWeather API."""
    try:
        params = {'q': location, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

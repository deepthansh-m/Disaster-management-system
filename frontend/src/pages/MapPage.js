import React, { useRef, useState, useEffect } from "react";
import L from "leaflet";
import { useNavigate } from "react-router-dom";
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import { getWeatherData } from "../services/api_service";

// Define default icon for markers
const defaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// Set default icon for all markers
L.Marker.prototype.options.icon = defaultIcon;

const MapPage = () => {
  const mapContainerRef = useRef(null);
  const navigate = useNavigate();
  const mapInstanceRef = useRef(null);
  const currentMarkerRef = useRef(null);

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [weatherData, setWeatherData] = useState(null);

  useEffect(() => {
    // Make sure the map container exists and has dimensions
    if (!mapInstanceRef.current && mapContainerRef.current) {
      // Initialize map
      mapInstanceRef.current = L.map(mapContainerRef.current, {
        center: [20, 0], // More interesting default center
        zoom: 2,
        minZoom: 2,
        maxZoom: 18,
        worldCopyJump: true // Allows continuous scrolling horizontally
      });

      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        noWrap: false
      }).addTo(mapInstanceRef.current);

      // Add click event listener
      mapInstanceRef.current.on('click', handleMapClick);
    }

    // Trigger a resize event after map initialization
    if (mapInstanceRef.current) {
      setTimeout(() => {
        mapInstanceRef.current.invalidateSize();
      }, 100);
    }

    // Cleanup function
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  const handleMapClick = async (event) => {
    const { lat, lng } = event.latlng;
    console.log('Clicked coordinates:', lat, lng);

    try {
      setIsLoading(true);
      setError(null);

      if (currentMarkerRef.current) {
        currentMarkerRef.current.remove();
      }

      currentMarkerRef.current = L.marker([lat, lng]).addTo(mapInstanceRef.current);

      const data = await getWeatherData(lat, lng);
      setWeatherData(data);
    } catch (err) {
      setError('Failed to fetch weather data.');
      console.error('Error fetching weather data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewDetails = () => {
    if (weatherData && currentMarkerRef.current) {
      const { lat, lng } = currentMarkerRef.current.getLatLng();
      
      // Ensure all values are valid numbers
      const params = {
        lat: isNaN(lat) ? '0' : lat.toFixed(6),
        lng: isNaN(lng) ? '0' : lng.toFixed(6),
        temp: isNaN(weatherData.temperatureCelsius) ? '0' : weatherData.temperatureCelsius.toFixed(2),
        pressure: isNaN(weatherData.pressure_hpa) ? '1013' : weatherData.pressure_hpa.toFixed(2),
        humidity: isNaN(weatherData.humidity_percent) ? '50' : weatherData.humidity_percent.toFixed(2),
        sea_level: isNaN(weatherData.sea_level_pressure) ? '1013' : weatherData.sea_level_pressure.toFixed(2),
        wind_speed: isNaN(weatherData.wind_speed_ms) ? '0' : weatherData.wind_speed_ms.toFixed(2)
      };
      
      const queryParams = new URLSearchParams(params).toString();
      navigate(`/details?${queryParams}`);
    }
  };

  return (
    <div className="flex flex-col h-screen p-4">
      {isLoading && (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white p-4 rounded-lg">Loading...</div>
        </div>
      )}
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <div 
        ref={mapContainerRef} 
        className="flex-grow w-full rounded-lg shadow-lg mb-4"
        style={{ minHeight: '500px' }}
      />
      
      {weatherData && (
        <div className="bg-white p-4 rounded-lg shadow-lg mt-4">
          <h3 className="text-xl font-bold mb-4">Weather Data</h3>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div>
              <p className="font-semibold">Temperature</p>
              <p>{weatherData.temperatureCelsius}°C</p>
            </div>
            <div>
              <p className="font-semibold">Pressure</p>
              <p>{weatherData.pressure_hpa} hPa</p>
            </div>
            <div>
              <p className="font-semibold">Humidity</p>
              <p>{weatherData.humidity_percent}%</p>
            </div>
            <div>
              <p className="font-semibold">Sea Level Pressure</p>
              <p>{weatherData.sea_level_pressure} hPa</p>
            </div>
            <div>
              <p className="font-semibold">Wind Speed</p>
              <p>{weatherData.wind_speed_ms} m/s</p>
            </div>
          </div>
          
          <button 
            onClick={handleViewDetails}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors"
          >
            View Disaster Prediction Details
          </button>
        </div>
      )}
    </div>
  );
};

export default MapPage;
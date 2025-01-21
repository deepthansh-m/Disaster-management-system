// api_service.js
const BASE_URL = 'http://localhost:5000';

export async function getWeatherData(latitude, longitude) {
    try {
        const response = await fetch(`${BASE_URL}/map/?lat=${latitude}&lon=${longitude}`, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to fetch weather data.');
        }
        
        // The backend now returns direct JSON fields: 
        // { temperatureCelsius, pressure_hpa, humidity_percent, sea_level_pressure, wind_speed_ms }
        const data = await response.json();
        
        return {
            temperatureCelsius: data.temperatureCelsius,
            pressure_hpa: data.pressure_hpa,
            humidity_percent: data.humidity_percent,
            sea_level_pressure: data.sea_level_pressure,
            wind_speed_ms: data.wind_speed_ms
        };
    } catch (error) {
        console.error('Error fetching weather data:', error);
        // Fallback values if API fetch fails
        return {
            temperatureCelsius: null,
            pressure_hpa: 1013,
            humidity_percent: 50,
            sea_level_pressure: 1013,
            wind_speed_ms: 0
        };
    }
}
export async function getDisasterPrediction({
    lat, lng, temp, pressure, humidity, wind_speed
}) {
    try {
        // Validate parameters
        if (!lat || !lng || !temp || !pressure || !humidity || !wind_speed) {
            throw new Error('Missing required parameters');
        }

        // Format parameters
        const params = new URLSearchParams({
            lat: parseFloat(lat).toFixed(6),
            lng: parseFloat(lng).toFixed(6),
            temp: parseFloat(temp).toFixed(2),
            pressure: parseFloat(pressure).toFixed(2),
            humidity: parseFloat(humidity).toFixed(2),
            wind_speed: parseFloat(wind_speed).toFixed(2),
        });

        const response = await fetch(`${BASE_URL}/details/?${params}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.details || data.error || 'Prediction request failed');
        }

        if (data.status !== 'success') {
            throw new Error('Invalid response from prediction service');
        }

        return {
            disaster_type: data.disaster_type || 'Unknown',
            predicted_deaths: parseInt(data.predicted_deaths) || 0,
            predicted_infra_loss: parseFloat(data.predicted_infra_loss) || 0,
            severity: parseFloat(data.severity) || 0,
            confidence: data.confidence || null,
            status: data.status
        };
    } catch (error) {
        console.error('Error fetching disaster prediction:', error);
        throw error;
    }
}

const handleResponse = async (response) => {
    const contentType = response.headers.get("content-type");
    if (!response.ok) {
        let errorMessage = 'API request failed';
        if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json();
            errorMessage = errorData.error || errorMessage;
        } else {
            errorMessage = await response.text() || errorMessage;
        }
        throw new Error(errorMessage);
    }
    return contentType && contentType.includes("application/json")
        ? response.json()
        : response.text();
};

const validateCoordinates = ({ latitude, longitude }) => {
    // Convert to numbers if they are strings
    const lat = typeof latitude === 'string' ? parseFloat(latitude) : latitude;
    const lng = typeof longitude === 'string' ? parseFloat(longitude) : longitude;

    // Check if conversion was successful
    if (isNaN(lat) || isNaN(lng)) {
        throw new Error('Latitude and longitude must be valid numbers');
    }

    // Validate latitude range
    if (lat < -90 || lat > 90) {
        throw new Error('Latitude must be between -90 and 90 degrees');
    }

    // Validate longitude range
    if (lng < -180 || lng > 180) {
        throw new Error('Longitude must be between -180 and 180 degrees');
    }

    return { latitude: lat, longitude: lng };
};

const apiService = {
    // Disaster CRUD operations
    getDisasters: async () => {
        const response = await fetch(`${BASE_URL}/disasters/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        return handleResponse(response);
    },

    getDisasterById: async (id) => {
        const response = await fetch(`${BASE_URL}/disasters/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        return handleResponse(response);
    },

    createDisaster: async (disasterData) => {
        const response = await fetch(`${BASE_URL}/disasters/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(disasterData)
        });
        return handleResponse(response);
    },

    updateDisaster: async (id, disasterData) => {
        const response = await fetch(`${BASE_URL}/disasters/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(disasterData)
        });
        return handleResponse(response);
    },

    deleteDisaster: async (id) => {
        const response = await fetch(`${BASE_URL}/disasters/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        return handleResponse(response);
    },

// Prediction operations
    getPrediction: async (requestData) => {
      try {
        const response = await fetch(`/api/predictions/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestData),
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Prediction request failed');
        }
  
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Prediction API Error:', error);
        throw error;
      }
    },
  

    // frontend/src/services/api_service.js
    getDisasterDetails : async ({ lat, lng, query = '' }) => {
    try {
        // Validate coordinates if provided
        if (lat && lng) {
            validateCoordinates({ 
                latitude: parseFloat(lat), 
                longitude: parseFloat(lng) 
            });
        }

        const params = new URLSearchParams({
            lat: lat || '',
            lng: lng || '',
            query: query
        });

        const response = await fetch(`${BASE_URL}/disaster?${params}/`, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        return handleResponse(response);
    } catch (error) {
        console.error('Disaster Details API Error:', error);
        throw error;
    }
},
     
};

export default apiService;
 
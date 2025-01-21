import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import apiService from '../services/api_service';
import DisasterPredictionChart from '../components/DisasterPredictionChart';

function DetailsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [disasterData, setDisasterData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [predictionData, setPredictionData] = useState([]);

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const lat = queryParams.get('lat');
    const lng = queryParams.get('lng');
    const query = queryParams.get('query');
    const address = queryParams.get('address');

    // Validate input
    if (!lat && !lng && !query) {
      setError('Invalid search parameters');
      setLoading(false);
      return;
    }

    const fetchDisasterDetails = async () => {
      try {
        setLoading(true);
        // Fetch disaster details based on available parameters
        const data = await apiService.getDisasterDetails({ 
          lat, 
          lng, 
          query,
          address
        });
        setDisasterData(data);

        // Fetch prediction data for the location
        const predictionData = await apiService.getPrediction(query || `${lat},${lng}`);
        setPredictionData(predictionData);
      } catch (error) {
        console.error('Failed to fetch disaster details:', error);
        setError(error.message || 'Unable to fetch location details');
      } finally {
        setLoading(false);
      }
    };

    fetchDisasterDetails();
  }, [location]);

  const handleGoBack = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl">Loading details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h2 className="text-2xl text-red-600 mb-4">Error</h2>
        <p>{error}</p>
        <button 
          onClick={handleGoBack}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="details-page container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold">Location Details</h2>
        <button 
          onClick={handleGoBack}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Back to Home
        </button>
      </div>

      {disasterData ? (
        <div className="details-content grid md:grid-cols-2 gap-6">
          <div className="disaster-info bg-gray-100 p-6 rounded-lg">
            <h3 className="text-2xl font-semibold mb-4">Disaster Information</h3>
            <div className="space-y-3">
              <p><strong>Location:</strong> {disasterData.location || 'Not specified'}</p>
              <p><strong>Risk Level:</strong> {disasterData.riskLevel || 'Unknown'}</p>
              <p><strong>Potential Hazards:</strong> {disasterData.hazards?.join(', ') || 'No specific hazards identified'}</p>
              {disasterData.additionalInfo && (
                <p><strong>Additional Info:</strong> {disasterData.additionalInfo}</p>
              )}
            </div>
          </div>

          <div className="prediction-section bg-gray-100 p-6 rounded-lg">
            <h3 className="text-2xl font-semibold mb-4">Disaster Prediction</h3>
            <DisasterPredictionChart data={predictionData} />
          </div>
        </div>
      ) : (
        <p className="text-center text-gray-600">No detailed information available for this location.</p>
      )}
    </div>
  );
}

export default DetailsPage;
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getDisasterPrediction } from '../services/api_service';

const DetailsPage = () => {
    const [searchParams] = useSearchParams();
    const [predictionData, setPredictionData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPrediction = async () => {
            try {
                // Include all 7 required parameters
                const params = ['lat', 'lng', 'temp', 'pressure', 'humidity', 'wind_speed'];
                const missingParams = params.filter(param => !searchParams.get(param));
                
                if (missingParams.length > 0) {
                    throw new Error(`Missing required parameters: ${missingParams.join(', ')}`);
                }

                const requestData = Object.fromEntries(
                    params.map(param => [param, searchParams.get(param)])
                );

                const data = await getDisasterPrediction(requestData);
                setPredictionData(data);
            } catch (err) {
                setError(err.message);
                console.error('Prediction error:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchPrediction();
    }, [searchParams]);
    // Function to determine severity class
    const getSeverityColor = (severity) => {
        const severityPercent = severity * 100;
        if (severityPercent >= 75) return 'bg-red-100 text-red-800 border-red-200';
        if (severityPercent >= 50) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
        return 'bg-green-100 text-green-800 border-green-200';
    };

    const getSeverityLabel = (severity) => {
        const severityPercent = severity * 100;
        if (severityPercent >= 75) return 'High Risk';
        if (severityPercent >= 50) return 'Medium Risk';
        return 'Low Risk';
    };
    const formatCurrency = (amount) => {
    if (isNaN(amount) || amount === null || amount === undefined) {
        console.debug('Invalid infrastructure loss value:', amount);
        return '$0';
    }
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(Math.max(0, amount));
};


    // Loading state
    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="animate-pulse text-xl">Loading prediction data...</div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="max-w-md p-4 bg-red-50 border border-red-200 rounded-lg">
                    <h2 className="text-xl font-semibold text-red-800 mb-2">Error</h2>
                    <p className="text-red-600">{error}</p>
                </div>
            </div>
        );
    }

        const renderPredictionData = () => {
            if (!predictionData) return null;
    
            return (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="border p-4 rounded">
                        <h2 className="font-semibold mb-2">Disaster Information</h2>
                        <p className="text-lg font-medium">{predictionData.disaster_type}</p>
                        <p className="mt-2">
                            <span className="text-gray-600">Predicted Deaths: </span>
                            {predictionData.predicted_deaths.toLocaleString()}
                        </p>
                        <p className="mt-2">
                            <span className="text-gray-600">Infrastructure Loss: </span>
                            {formatCurrency(Number(predictionData.predicted_infra_loss))}
                        </p>
                    </div>
                      {/* Severity Display */}
                      <div className={`mt-4 p-4 rounded-lg border ${getSeverityColor(predictionData.severity)}`}>
                            <div className="flex justify-between items-center">
                                <span className="font-medium">Severity Level:</span>
                                <span className="font-bold">
                                    {getSeverityLabel(predictionData.severity)}
                                </span>
                            </div>
                            <div className="mt-2">
                                <div className="w-full bg-gray-200 rounded-full h-2.5">
                                    <div 
                                        className="bg-red-600 h-2.5 rounded-full transition-all duration-500"
                                        style={{ width: `${predictionData.severity * 100}%` }}
                                    ></div>
                                </div>
                                <p className="text-sm mt-1 text-right">
                                    {(predictionData.severity * 100).toFixed(1)}%
                                </p>
                            </div>
                        </div>
    
                    <div className="border p-4 rounded">
                        <h2 className="font-semibold mb-2">Weather Parameters</h2>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-gray-600">Temperature</p>
                                <p>{parseFloat(searchParams.get('temp')).toFixed(1)}°C</p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Pressure</p>
                                <p>{parseFloat(searchParams.get('pressure')).toFixed(1)} hPa</p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Humidity</p>
                                <p>{parseFloat(searchParams.get('humidity')).toFixed(1)}%</p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Wind Speed</p>
                                <p>{parseFloat(searchParams.get('wind_speed')).toFixed(1)} m/s</p>
                            </div>
                        </div>
                    </div>
                </div>
            );
        };
    
        return (
            <div className="p-4">
                <h1 className="text-2xl font-bold mb-4">Disaster Prediction Details</h1>
                {loading ? (
                    <div>Loading...</div>
                ) : error ? (
                    <div className="text-red-600">{error}</div>
                ) : (
                    renderPredictionData()
                )}
            </div>
        );
    };
    
    export default DetailsPage;
import React from "react";

function DisasterDetails({ data }) {
  // Handle case when no data is provided
  if (!data) {
    return (
      <div className="p-4 text-center text-gray-600 bg-gray-100 rounded-lg">
        No disaster details available.
      </div>
    );
  }

  return (
    <div className="disaster-details bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">
        {data.name || 'Disaster Information'}
      </h2>
      
      <div className="space-y-3 text-gray-700">
        <DetailRow 
          label="Location" 
          value={data.location || 'Not specified'}
        />
        <DetailRow 
          label="Severity" 
          value={data.severity || 'Unknown'}
        />
        <DetailRow 
          label="Description" 
          value={data.description || 'No description available'}
        />
        <DetailRow 
          label="Possible Deaths" 
          value={data.possibleDeaths !== undefined 
            ? data.possibleDeaths.toLocaleString() 
            : 'Not estimated'}
        />
        <DetailRow 
          label="Infrastructure Loss" 
          value={data.infrastructureLoss || 'Not assessed'}
        />
        <DetailRow 
          label="Food Supplies Required" 
          value={data.foodSuppliesRequired || 'Not determined'}
        />
      </div>
    </div>
  );
}

// Helper component to create consistent row formatting
function DetailRow({ label, value }) {
  return (
    <div className="flex justify-between">
      <span className="font-semibold">{label}:</span>
      <span>{value}</span>
    </div>
  );
}

export default DisasterDetails;
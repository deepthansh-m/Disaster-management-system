import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const WorldMap = ({ onLocationSelect }) => {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);

  useEffect(() => {
    // Initialize map if not already initialized
    if (!mapRef.current) return;

    const mapInstance = L.map(mapRef.current).setView([0, 0], 2);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapInstance);

    // Add click event to show location details
    mapInstance.on('click', async (event) => {
      const { lat, lng } = event.latlng;

      try {
        // Reverse geocoding to get address
        const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`);
        const data = await response.json();
        
        // Create popup with location details
        const popup = L.popup()
          .setLatLng([lat, lng])
          .setContent(`
            <div>
              <p><strong>Latitude:</strong> ${lat.toFixed(4)}</p>
              <p><strong>Longitude:</strong> ${lng.toFixed(4)}</p>
              <p><strong>Address:</strong> ${data.display_name || 'Address not found'}</p>
              <button id="view-details-btn" class="bg-blue-500 text-white px-2 py-1 rounded mt-2">View Details</button>
            </div>
          `)
          .openOn(mapInstance);

        // Add click event listener to the button
        setTimeout(() => {
          const viewDetailsBtn = document.getElementById('view-details-btn');
          if (viewDetailsBtn) {
            viewDetailsBtn.addEventListener('click', () => {
              onLocationSelect({ lat, lng, address: data.display_name });
            });
          }
        }, 0);
      } catch (error) {
        console.error('Error fetching location details:', error);
        
        // Fallback popup if geocoding fails
        const popup = L.popup()
          .setLatLng([lat, lng])
          .setContent(`
            <div>
              <p><strong>Latitude:</strong> ${lat.toFixed(4)}</p>
              <p><strong>Longitude:</strong> ${lng.toFixed(4)}</p>
              <button id="view-details-btn" class="bg-blue-500 text-white px-2 py-1 rounded mt-2">View Details</button>
            </div>
          `)
          .openOn(mapInstance);

        // Add click event listener to the button
        setTimeout(() => {
          const viewDetailsBtn = document.getElementById('view-details-btn');
          if (viewDetailsBtn) {
            viewDetailsBtn.addEventListener('click', () => {
              onLocationSelect({ lat, lng });
            });
          }
        }, 0);
      }
    });

    setMap(mapInstance);

    // Cleanup on unmount
    return () => {
      mapInstance.remove();
    };
  }, [onLocationSelect]);

  return (
    <div 
      ref={mapRef} 
      className="world-map w-full h-[500px] mt-4"
    />
  );
};

export default WorldMap;
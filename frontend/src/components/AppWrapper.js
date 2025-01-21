// src/App.js or your main wrapper component
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import MapPage from '../pages/MapPage';
import DetailsPage from '../pages/DetailsPage';
import '../styles/main.css';

const AppWrapper = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState('home');
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    const path = location.pathname.split('/')[1] || 'home';
    setCurrentPage(path);
  }, [location]);

  const handleNavigation = (path) => {
    setIsTransitioning(true);
    setTimeout(() => {
      navigate(path);
      setIsTransitioning(false);
    }, 300);
  };

  return (
    <div className="min-h-screen bg-green-50">
      {/* Header */}
      {currentPage === 'home' && !isTransitioning && (
        <header className="bg-white shadow-sm">
          <nav className="container mx-auto px-4 py-4">
            <div className="flex justify-between items-center">
              <h1 className="text-2xl font-bold text-gray-800">
                Disaster Prediction System
              </h1>
              <div className="space-x-6">
                <button 
                  onClick={() => handleNavigation('/')}
                  className="text-gray-600 hover:text-emerald-600"
                >
                  Home
                </button>
                <button 
                  onClick={() => handleNavigation('/map')}
                  className="text-gray-600 hover:text-emerald-600"
                >
                  Map
                </button>
                <button 
                  onClick={() => handleNavigation('/details')}
                  className="text-gray-600 hover:text-emerald-600"
                >
                  View Prediction
                </button>
              </div>
            </div>
          </nav>
        </header>
      )}

      {/* Main content */}
      <main className={`transition-opacity duration-300 ${isTransitioning ? 'opacity-0' : 'opacity-100'}`}>
        {currentPage === 'home' && <HomePage />}
        {currentPage === 'map' && <MapPage />}
        {currentPage === 'details' && <DetailsPage />}
      </main>
    </div>
  );
};

export default AppWrapper;
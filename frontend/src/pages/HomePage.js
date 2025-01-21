import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, AlertTriangle, Droplet, Flame, ArrowRight } from 'lucide-react';
import '../styles/output.css'

const HomePage = () => {
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(path);
  };

  const DisasterCard = ({ title, description, imageUrl, alignment }) => {
    const [imageLoading, setImageLoading] = React.useState(true);
    const [imageError, setImageError] = React.useState(false);
  
    return (
      <div className={`flex flex-col md:flex-row items-center gap-8 my-12 ${
        alignment === 'right' ? 'md:flex-row-reverse' : ''
      }`}>
        <div className="w-full md:w-1/2 relative">
          {imageLoading && (
            <div className="absolute inset-0 bg-gray-200 animate-pulse rounded-lg"/>
          )}
          <img
            src={imageUrl}
            alt={title}
            className={`w-full h-[300px] object-cover rounded-lg shadow-lg transition-opacity duration-300 ${
              imageLoading ? 'opacity-0' : 'opacity-100'
            }`}
            onLoad={() => setImageLoading(false)}
            onError={() => {
              setImageError(true);
              setImageLoading(false);
            }}
          />
          {imageError && (
            <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
              <span className="text-gray-500">Image not available</span>
            </div>
          )}
        </div>
        <div className="w-full md:w-1/2">
          <h3 className="text-2xl font-bold mb-4">{title}</h3>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>
    );
  };
  
  return (
    <div className="min-h-screen bg-green-50">
      {/* Header */}
      

      {/* Hero Section */}
      <section className="bg-gradient-to-b from-emerald-600 to-green-50 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Predict • Prepare • Protect
          </h2>
          <p className="text-xl mb-8 max-w-3xl mx-auto text-green-100">
            Advanced analytics and real-time monitoring system to predict and prepare for natural disasters.
            Protecting communities through early warning and preparation.
          </p>
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => handleNavigation('/map')}
              className="bg-white text-emerald-600 px-8 py-4 rounded-md font-semibold hover:bg-green-100 transition-colors"
            >
              View Map
            </button>
            <button
              onClick={() => handleNavigation('/details')}
              className="border-2 border-white text-white px-8 py-4 rounded-md font-semibold hover:bg-emerald-700 transition-colors"
            >
              Get Predictions
            </button>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-16 text-gray-800">
          Monitor Different Types of Disasters
        </h2>
        
        <DisasterCard
          title="Earthquake Monitoring"
          description="Our advanced seismic monitoring system provides real-time tracking of tectonic movements and potential earthquake zones."
          imageUrl="hhttps://images.unsplash.com/photo-1536529289256-9eeff3c43741?auto=format&fit=crop&q=80&w=1000"
          alignment="left"
        />

        <DisasterCard
          title="Flood Detection"
          description="Advanced water level monitoring and rainfall prediction systems to prevent flood damage."
          imageUrl="https://images.unsplash.com/photo-1547683905-f686c993aae5"
          alignment="right"
        />

        <DisasterCard
          title="Wildfire Detection"
          description="Satellite-based detection system for monitoring high-risk areas and predicting fire spread patterns."
          imageUrl=""
          alignment="left"
        />
      </main>


      {/* Features Section */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "24/7 Monitoring",
                description: "Continuous surveillance of environmental parameters and seismic activities",
                icon: AlertTriangle
              },
              {
                title: "AI-Powered Analytics",
                description: "Advanced algorithms providing accurate disaster predictions and risk assessments",
                icon: MapPin
              },
              {
                title: "Early Warning System",
                description: "Immediate alerts and notifications for potentially affected areas",
                icon: Flame
              }
            ].map((feature, index) => (
              <div 
                key={index}
                className="bg-green-50 p-8 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
              >
                <feature.icon className="w-8 h-8 text-emerald-600 mb-4" />
                <h3 className="text-xl font-semibold mb-3 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-emerald-600 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="font-bold text-lg mb-4">About Us</h3>
              <p className="text-green-100">
                Dedicated to protecting communities through advanced disaster prediction and prevention systems.
              </p>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <button onClick={() => handleNavigation('/map')} className="text-green-100 hover:text-white">
                    Interactive Map
                  </button>
                </li>
                <li>
                  <button onClick={() => handleNavigation('/details')} className="text-green-100 hover:text-white">
                    Prediction System
                  </button>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">Contact</h3>
              <p className="text-green-100">
                Email: info@disasterprediction.com<br />
                Phone: (555) 123-4567
              </p>
            </div>
          </div>
          <div className="border-t border-green-500 mt-8 pt-8 text-center">
            <p className="text-green-100">© 2025 Disaster Prediction System. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
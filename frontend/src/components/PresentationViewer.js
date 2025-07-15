import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PresentationViewer = () => {
  const [presentation, setPresentation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPresentation();
  }, []);

  const fetchPresentation = async () => {
    try {
      const response = await axios.get(`${API}/presentation`);
      setPresentation(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load presentation");
      setLoading(false);
    }
  };

  const nextSlide = () => {
    if (currentSlide < presentation?.slides?.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  const prevSlide = () => {
    if (currentSlide > 0) {
      setCurrentSlide(currentSlide - 1);
    }
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  const renderSlideContent = (content) => {
    return content.split('\n').map((line, index) => {
      if (line.trim() === '') return <br key={index} />;
      
      if (line.startsWith('# ')) {
        return <h1 key={index} className="text-4xl font-bold mb-4 text-white">{line.replace('# ', '')}</h1>;
      }
      
      if (line.startsWith('## ')) {
        return <h2 key={index} className="text-3xl font-bold mb-4 text-blue-300">{line.replace('## ', '')}</h2>;
      }
      
      if (line.startsWith('### ')) {
        return <h3 key={index} className="text-2xl font-semibold mb-3 text-green-300">{line.replace('### ', '')}</h3>;
      }
      
      if (line.startsWith('**') && line.endsWith('**')) {
        return <p key={index} className="text-xl font-bold mb-2 text-yellow-300">{line.replace(/\*\*/g, '')}</p>;
      }
      
      if (line.startsWith('*') && !line.startsWith('**')) {
        return <p key={index} className="text-lg mb-2 text-gray-300 italic">{line.replace(/^\*/, '')}</p>;
      }
      
      if (line.startsWith('- ')) {
        return <li key={index} className="text-lg mb-2 text-white ml-4">{line.replace('- ', '')}</li>;
      }
      
      if (line.startsWith('---')) {
        return <hr key={index} className="my-4 border-gray-500" />;
      }
      
      return <p key={index} className="text-lg mb-2 text-white">{line}</p>;
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-300">Loading presentation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <Link to="/" className="text-purple-400 hover:underline">← Back to Home</Link>
        </div>
      </div>
    );
  }

  const slide = presentation?.slides?.[currentSlide];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="text-purple-400 hover:text-purple-300 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Home
            </Link>
            <div className="flex items-center space-x-4">
              <span className="text-white">
                {currentSlide + 1} / {presentation?.slides?.length}
              </span>
              <Link to="/whitepaper" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Read Paper
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Slide Navigation */}
          <div className="lg:w-1/4">
            <div className="bg-black/20 backdrop-blur-sm rounded-lg p-6 border border-white/10">
              <h3 className="text-lg font-semibold mb-4 text-white">Slides</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {presentation?.slides?.map((slide, index) => (
                  <button
                    key={index}
                    onClick={() => goToSlide(index)}
                    className={`text-left w-full px-3 py-2 rounded text-sm transition-colors ${
                      currentSlide === index 
                        ? 'bg-purple-600 text-white' 
                        : 'text-gray-300 hover:bg-white/10'
                    }`}
                  >
                    {index + 1}. {slide.title}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Slide */}
          <div className="lg:w-3/4">
            <div className="bg-black/30 backdrop-blur-sm rounded-lg p-8 border border-white/10 min-h-[600px]">
              <div className="mb-8">
                <div className="text-center">
                  {slide && renderSlideContent(slide.content)}
                </div>
              </div>

              {/* Navigation Controls */}
              <div className="flex justify-between items-center mt-8 pt-6 border-t border-white/10">
                <button
                  onClick={prevSlide}
                  disabled={currentSlide === 0}
                  className="flex items-center px-6 py-3 bg-white/10 text-white rounded-lg hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  Previous
                </button>

                <div className="flex space-x-2">
                  {presentation?.slides?.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => goToSlide(index)}
                      className={`w-3 h-3 rounded-full transition-colors ${
                        index === currentSlide ? 'bg-purple-400' : 'bg-white/30'
                      }`}
                    />
                  ))}
                </div>

                <button
                  onClick={nextSlide}
                  disabled={currentSlide === presentation?.slides?.length - 1}
                  className="flex items-center px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Next
                  <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Slide Notes */}
            {slide?.notes && (
              <div className="mt-4 bg-black/20 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                <h4 className="text-sm font-semibold text-gray-300 mb-2">Speaker Notes:</h4>
                <p className="text-sm text-gray-400">{slide.notes}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Keyboard Navigation */}
      <div className="fixed bottom-4 right-4 bg-black/40 backdrop-blur-sm rounded-lg p-3 border border-white/10">
        <div className="text-xs text-gray-400">
          <p>← → Arrow keys to navigate</p>
          <p>ESC to return home</p>
        </div>
      </div>
    </div>
  );
};

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
  if (window.location.pathname === '/presentation') {
    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault();
        // This would need to be handled by the component
        break;
      case 'ArrowRight':
        e.preventDefault();
        // This would need to be handled by the component
        break;
      case 'Escape':
        window.location.href = '/';
        break;
    }
  }
});

export default PresentationViewer;
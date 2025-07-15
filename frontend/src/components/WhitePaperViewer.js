import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const WhitePaperViewer = () => {
  const [whitePaper, setWhitePaper] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchWhitePaper();
  }, []);

  const fetchWhitePaper = async () => {
    try {
      const response = await axios.get(`${API}/whitepaper`);
      setWhitePaper(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load white paper");
      setLoading(false);
    }
  };

  const renderFigure = (figure) => {
    if (figure.svg_content) {
      return (
        <div className="my-8 p-4 bg-gray-50 rounded-lg">
          <div className="text-center">
            <div dangerouslySetInnerHTML={{ __html: figure.svg_content }} />
            <p className="text-sm text-gray-600 mt-4 font-medium">{figure.caption}</p>
          </div>
        </div>
      );
    }
    return null;
  };

  const renderContent = (content) => {
    return content.split('\n').map((paragraph, index) => {
      if (paragraph.trim() === '') return null;
      
      if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
        return <h4 key={index} className="text-lg font-semibold mt-6 mb-3 text-blue-800">{paragraph.replace(/\*\*/g, '')}</h4>;
      }
      
      if (paragraph.startsWith('*') && paragraph.endsWith('*')) {
        return <h5 key={index} className="text-md font-medium mt-4 mb-2 text-gray-700">{paragraph.replace(/\*/g, '')}</h5>;
      }
      
      if (paragraph.startsWith('```') && paragraph.endsWith('```')) {
        return <pre key={index} className="bg-gray-100 p-4 rounded-lg my-4 text-sm overflow-x-auto"><code>{paragraph.replace(/```/g, '')}</code></pre>;
      }
      
      return <p key={index} className="mb-4 text-gray-700 leading-relaxed">{paragraph}</p>;
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading revolutionary white paper...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <Link to="/" className="text-blue-600 hover:underline">← Back to Home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="text-blue-600 hover:text-blue-800 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Home
            </Link>
            <div className="flex space-x-4">
              <Link to="/presentation" className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                View Presentation
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Table of Contents */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-sm p-6 sticky top-4">
              <h3 className="text-lg font-semibold mb-4 text-gray-800">Table of Contents</h3>
              <ul className="space-y-2">
                <li>
                  <button
                    onClick={() => setActiveSection(-1)}
                    className={`text-left w-full px-3 py-2 rounded text-sm transition-colors ${
                      activeSection === -1 ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Abstract
                  </button>
                </li>
                {whitePaper?.sections?.map((section, index) => (
                  <li key={index}>
                    <button
                      onClick={() => setActiveSection(index)}
                      className={`text-left w-full px-3 py-2 rounded text-sm transition-colors ${
                        activeSection === index ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {section.title}
                    </button>
                  </li>
                ))}
                <li>
                  <button
                    onClick={() => setActiveSection(-2)}
                    className={`text-left w-full px-3 py-2 rounded text-sm transition-colors ${
                      activeSection === -2 ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    References
                  </button>
                </li>
              </ul>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            <div className="bg-white rounded-lg shadow-sm p-8">
              {/* Paper Header */}
              <div className="mb-8 border-b pb-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">
                  {whitePaper?.title}
                </h1>
                <div className="space-y-2">
                  {whitePaper?.authors?.map((author, index) => (
                    <div key={index} className="text-gray-600">
                      <span className="font-medium">{author.name}</span>
                      <span className="text-sm"> - {author.affiliation}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-4">
                  <div className="flex flex-wrap gap-2">
                    {whitePaper?.keywords?.map((keyword, index) => (
                      <span key={index} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Content Display */}
              {activeSection === -1 && (
                <div>
                  <h2 className="text-2xl font-bold mb-4 text-gray-900">Abstract</h2>
                  <div className="text-gray-700 leading-relaxed">
                    {renderContent(whitePaper?.abstract || "")}
                  </div>
                </div>
              )}

              {activeSection === -2 && (
                <div>
                  <h2 className="text-2xl font-bold mb-4 text-gray-900">References</h2>
                  <div className="space-y-4">
                    {whitePaper?.references?.map((ref, index) => (
                      <div key={index} className="border-l-4 border-blue-200 pl-4">
                        <p className="text-gray-700">
                          <span className="font-medium">{ref.title}</span>
                          <br />
                          <span className="text-sm">{ref.authors.join(", ")} ({ref.year})</span>
                          <br />
                          <span className="text-sm italic">{ref.journal}</span>
                          {ref.doi && (
                            <>
                              <br />
                              <span className="text-sm text-blue-600">DOI: {ref.doi}</span>
                            </>
                          )}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeSection >= 0 && whitePaper?.sections?.[activeSection] && (
                <div>
                  <h2 className="text-2xl font-bold mb-6 text-gray-900">
                    {whitePaper.sections[activeSection].title}
                  </h2>
                  <div className="text-gray-700 leading-relaxed">
                    {renderContent(whitePaper.sections[activeSection].content)}
                  </div>
                  
                  {/* Figures */}
                  {whitePaper.sections[activeSection].figures?.map((figure, figIndex) => (
                    <div key={figIndex}>
                      {renderFigure(figure)}
                    </div>
                  ))}
                </div>
              )}

              {/* Navigation */}
              <div className="mt-8 pt-6 border-t flex justify-between">
                <button
                  onClick={() => setActiveSection(Math.max(-1, activeSection - 1))}
                  disabled={activeSection === -1}
                  className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  Previous
                </button>
                <button
                  onClick={() => setActiveSection(Math.min(whitePaper?.sections?.length - 1, activeSection + 1))}
                  disabled={activeSection === whitePaper?.sections?.length - 1}
                  className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Next
                  <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WhitePaperViewer;
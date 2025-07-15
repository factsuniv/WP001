import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import axios from "axios";
import WhitePaperViewer from "./components/WhitePaperViewer";
import PresentationViewer from "./components/PresentationViewer";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState("Checking...");

  const checkApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      setApiStatus("Connected to THPU API");
      console.log(response.data.message);
    } catch (e) {
      setApiStatus("API connection failed");
      console.error(e, `errored out requesting / api`);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkApi();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold text-white mb-4">
            Temporal-Holographic Processing Units
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            A Revolutionary Computing Architecture for the AI Era
          </p>
          <div className="flex justify-center space-x-4 mb-8">
            <span className={`px-4 py-2 rounded-full text-sm font-medium ${
              apiStatus === "Connected to THPU API" 
                ? "bg-green-900 text-green-300" 
                : "bg-red-900 text-red-300"
            }`}>
              {apiStatus}
            </span>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <Link to="/whitepaper" className="group">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 hover:bg-white/20 transition-all duration-300 transform hover:scale-105 border border-white/20">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Academic White Paper</h3>
                <p className="text-gray-300 mb-4">
                  Comprehensive technical analysis of THPU architecture, theoretical foundations, and performance projections
                </p>
                <div className="bg-blue-600 text-white px-4 py-2 rounded-full inline-block group-hover:bg-blue-700 transition-colors">
                  Read White Paper →
                </div>
              </div>
            </div>
          </Link>

          <Link to="/presentation" className="group">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 hover:bg-white/20 transition-all duration-300 transform hover:scale-105 border border-white/20">
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2h3a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1h3zM9 4h6V3H9v1zm-4 3v11h14V7H5z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Presentation Deck</h3>
                <p className="text-gray-300 mb-4">
                  Interactive presentation showcasing THPU innovations, applications, and market impact
                </p>
                <div className="bg-purple-600 text-white px-4 py-2 rounded-full inline-block group-hover:bg-purple-700 transition-colors">
                  View Presentation →
                </div>
              </div>
            </div>
          </Link>
        </div>

        <div className="mt-16 text-center">
          <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
            <h2 className="text-3xl font-bold text-white mb-4">Revolutionary Computing Technology</h2>
            <div className="grid md:grid-cols-4 gap-6 mt-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">1000x</div>
                <div className="text-gray-300">Energy Efficiency</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400 mb-2">100x</div>
                <div className="text-gray-300">Throughput Increase</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400 mb-2">10x</div>
                <div className="text-gray-300">Latency Reduction</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-red-400 mb-2">∞</div>
                <div className="text-gray-300">Adaptability</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-gray-400">
            © 2024 Advanced Computing Research Institute. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/whitepaper" element={<WhitePaperViewer />} />
          <Route path="/presentation" element={<PresentationViewer />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
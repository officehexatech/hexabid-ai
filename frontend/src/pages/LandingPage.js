import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import AIChatbot from '../components/AIChatbot';
import WhatsAppButton from '../components/WhatsAppButton';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const LandingPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [showDemo, setShowDemo] = useState(false);
  const [settings, setSettings] = useState(null);

  useEffect(() => {
    if (user) navigate('/dashboard');
  }, [user, navigate]);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await axios.get(`${API_URL}/settings/public`);
        setSettings(response.data);
      } catch (error) {
        console.error('Failed to fetch settings:', error);
      }
    };
    fetchSettings();
  }, []);

  return (
    <div className="min-h-screen bg-white">
      {/* Government Theme Bar */}
      <div className="bg-gradient-to-r from-orange-500 via-white to-green-600 h-1"></div>
      
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b sticky top-0 z-50 backdrop-blur-sm bg-white/95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <img src="https://customer-assets.emergentagent.com/job_tender-master-4/artifacts/9595dbly_1%20HexaBid%20Logo%20Sm.jpg" alt="HexaBid" className="h-12 w-auto" />
              <div>
                <span className="text-2xl font-bold text-gray-900">HexaBid</span>
                <p className="text-xs text-gray-600">AI-Powered Tender ERP</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button onClick={() => navigate('/login')} className="text-gray-700 hover:text-gray-900 px-4 py-2 rounded-md text-sm font-medium border border-gray-300">Sign In</button>
              <button onClick={() => navigate('/register')} className="bg-blue-600 text-white hover:bg-blue-700 px-6 py-2 rounded-md text-sm font-semibold shadow-md">Start Free →</button>
            </div>
          </div>
        </div>
      </nav>

      {/* 1. Hero Section */}
      <div className="bg-gradient-to-b from-blue-50 to-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>
                  Make in India • AI-Enabled
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold">GeM Ready</span>
              </div>
              <h1 className="text-5xl font-extrabold text-gray-900 leading-tight mb-6">
                AI-Powered Tender Bidding & 
                <span className="block text-blue-600 mt-2">Document Automation</span>
              </h1>
              <p className="text-xl text-gray-600 mb-4 leading-relaxed">
                Discover, Prepare & Submit Tenders <span className="font-bold text-blue-600">10x Faster</span> — With Zero Errors.
              </p>
              
              <div className="bg-orange-50 border-l-4 border-orange-500 p-4 mb-6">
                <p className="text-sm font-bold text-orange-700">🎉 100% FREE Forever • No Trial Period • Start Immediately</p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 mb-6">
                <button onClick={() => navigate('/register')} className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-bold hover:bg-blue-700 shadow-lg flex items-center justify-center">
                  Start Free <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
                </button>
                <button onClick={() => setShowDemo(true)} className="bg-white text-gray-700 px-8 py-4 rounded-lg text-lg font-semibold border-2 border-gray-300 hover:bg-gray-50">Watch Demo</button>
              </div>

              <div className="flex items-center space-x-6 text-sm text-gray-600">
                <div className="flex items-center"><svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>SSL Secure</div>
                <div className="flex items-center"><svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>Govt/PSU Ready</div>
                <div className="flex items-center"><svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>24/7 Available</div>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white p-6 rounded-2xl shadow-2xl border-4 border-blue-100">
                <div className="space-y-3">
                  {['GEM Portal Auto-Sync', 'AI BOQ Generator', 'Smart Vendor Network', 'Auto Document Pack', 'Price Intelligence'].map((f, i) => (
                    <div key={i} className="flex items-center space-x-3 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center"><svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg></div>
                      <span className="font-semibold text-gray-800">{f}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div><div className="text-3xl font-bold text-blue-400">10x</div><div className="text-sm text-gray-400">Faster Bidding</div></div>
          <div><div className="text-3xl font-bold text-green-400">Zero</div><div className="text-sm text-gray-400">Manual Errors</div></div>
          <div><div className="text-3xl font-bold text-purple-400">100%</div><div className="text-sm text-gray-400">Free Forever</div></div>
          <div><div className="text-3xl font-bold text-orange-400">24/7</div><div className="text-sm text-gray-400">AI Support</div></div>
        </div>
      </div>

      {/* 2. Why HexaBid - Pain → Solution */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why HexaBid?</h2>
            <p className="text-xl text-gray-600">From Tender Chaos to Complete Control</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {[
              {pain: 'Missing Important Tenders', solution: 'Auto-Fetch from GeM + All Portals', icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'},
              {pain: 'Hours on BOQ Preparation', solution: 'AI Generates BOQ in Minutes', icon: 'M13 10V3L4 14h7v7l9-11h-7z'},
              {pain: 'Technical Compliance Errors', solution: 'AI Auto-Compliance Check', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'},
              {pain: 'OEM Follow-up Nightmare', solution: 'Automated RFQ & Quote Tracking', icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'},
              {pain: 'Repetitive Document Creation', solution: 'One-Click Document Assembly', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'},
              {pain: 'Manual Deadline Tracking', solution: 'Smart Alerts & Reminders', icon: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9'},
              {pain: 'No Pricing Intelligence', solution: 'AI Price Suggestions + Analytics', icon: 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z'},
              {pain: 'Lost in Spreadsheets', solution: 'Central Workspace + MIS Dashboard', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'},
            ].map((item, idx) => (
              <div key={idx} className="flex items-start space-x-4 p-6 bg-gradient-to-r from-red-50 to-green-50 rounded-xl border-l-4 border-blue-500">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-2">
                    <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} /></svg>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="text-red-600 font-semibold mb-2 line-through">❌ {item.pain}</div>
                  <div className="text-green-700 font-bold text-lg">✅ {item.solution}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 3. Platform Overview */}
      <div className="bg-gradient-to-b from-blue-900 to-indigo-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Complete Tender Lifecycle Platform</h2>
            <p className="text-xl text-blue-200">10 Powerful Modules in One Platform</p>
          </div>

          <div className="grid md:grid-cols-5 gap-4">
            {[
              {icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z', title: 'Tender Discovery', desc: 'GeM + Portals'},
              {icon: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z', title: 'AI Parsing', desc: 'Smart Extract'},
              {icon: 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z', title: 'BOQ Engine', desc: 'Auto-Generate'},
              {icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z', title: 'Compliance', desc: 'AI Check'},
              {icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z', title: 'OEM RFQ', desc: 'Quote Track'},
              {icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z', title: 'Doc Assembly', desc: 'One-Click'},
              {icon: 'M13 10V3L4 14h7v7l9-11h-7z', title: 'AI Pricing', desc: 'Smart Suggest'},
              {icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z', title: 'Analytics', desc: 'MIS Reports'},
              {icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4', title: 'ERP Suite', desc: '6 Modules'},
              {icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z', title: 'Multi-Tenant', desc: 'Team Collab'},
            ].map((m, i) => (
              <div key={i} className="bg-white/10 backdrop-blur-sm p-6 rounded-xl text-center hover:bg-white/20 transition">
                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={m.icon} /></svg>
                </div>
                <h3 className="font-bold mb-1">{m.title}</h3>
                <p className="text-sm text-blue-200">{m.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 4. AI Features Spotlight */}
      <div className="py-20 bg-gradient-to-b from-purple-50 to-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <div className="inline-block px-4 py-2 bg-purple-100 text-purple-800 rounded-full font-semibold mb-4">🤖 AI-Powered Intelligence</div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Your AI Tender Assistant</h2>
            <p className="text-xl text-gray-600">Ask AI. Get Answers. Win Tenders.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-2xl shadow-xl border-2 border-purple-100">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI Chat Assistant</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start"><span className="text-purple-500 mr-2">•</span>"Create BOQ for this tender"</li>
                <li className="flex items-start"><span className="text-purple-500 mr-2">•</span>"Suggest compliant products"</li>
                <li className="flex items-start"><span className="text-purple-500 mr-2">•</span>"Draft technical compliance"</li>
                <li className="flex items-start"><span className="text-purple-500 mr-2">•</span>"Give me price suggestion"</li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-xl border-2 border-blue-100">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI OCR Engine</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start"><span className="text-blue-500 mr-2">•</span>Extract data from tender PDFs</li>
                <li className="flex items-start"><span className="text-blue-500 mr-2">•</span>Read OEM quote documents</li>
                <li className="flex items-start"><span className="text-blue-500 mr-2">•</span>Parse forms & annexures</li>
                <li className="flex items-start"><span className="text-blue-500 mr-2">•</span>Auto-fill into workspace</li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-xl border-2 border-green-100">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI Analytics</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start"><span className="text-green-500 mr-2">•</span>Pricing trend insights</li>
                <li className="flex items-start"><span className="text-green-500 mr-2">•</span>Competition pattern analysis</li>
                <li className="flex items-start"><span className="text-green-500 mr-2">•</span>Win probability calculator</li>
                <li className="flex items-start"><span className="text-green-500 mr-2">•</span>Margin optimization</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* 5. How It Works */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How HexaBid Works</h2>
            <p className="text-xl text-gray-600">From Tender Discovery to Submission in 7 Simple Steps</p>
          </div>

          <div className="relative">
            {/* Timeline line */}
            <div className="hidden md:block absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-blue-200"></div>

            {[
              {step: 1, title: 'Search & Discover', desc: 'Auto-fetch tenders from GeM + portals', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'},
              {step: 2, title: 'AI Parses Tender', desc: 'Extract BOQ, specs, eligibility', icon: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z'},
              {step: 3, title: 'Workspace Created', desc: 'Central hub with all tender data', icon: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z'},
              {step: 4, title: 'BOQ + Compliance', desc: 'AI generates and validates', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'},
              {step: 5, title: 'Collect OEM Quotes', desc: 'Send RFQ, track responses', icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'},
              {step: 6, title: 'Document Pack', desc: 'Generate all submission docs', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'},
              {step: 7, title: 'Submit & Track', desc: 'Monitor status & deadlines', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'},
            ].map((item, idx) => (
              <div key={idx} className={`flex items-center mb-8 ${idx % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                <div className={`w-full md:w-5/12 ${idx % 2 === 0 ? 'md:text-right md:pr-8' : 'md:text-left md:pl-8'}`}>
                  <div className="bg-white p-6 rounded-xl shadow-lg border-2 border-blue-100">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{item.title}</h3>
                    <p className="text-gray-600">{item.desc}</p>
                  </div>
                </div>
                <div className="relative flex items-center justify-center w-full md:w-2/12">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center shadow-xl z-10">
                    <span className="text-white font-bold text-xl">{item.step}</span>
                  </div>
                </div>
                <div className="w-full md:w-5/12"></div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 6. Use Cases */}
      <div className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Built for Every Tender Professional</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {title: 'Government Contractors', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4', desc: 'PSU & Govt tenders, compliance automation, bid management'},
              {title: 'Tender Consultants', icon: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z', desc: 'Multi-client management, white-label reports, collaboration tools'},
              {title: 'OEMs & Distributors', icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4', desc: 'Product catalog, RFQ tracking, quote management, dealer network'},
              {title: 'EPC Companies', icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z', desc: 'Project costing, subcontractor management, execution tracking'},
              {title: 'Service Contractors', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z', desc: 'AMC bidding, manpower costing, compliance management'},
              {title: 'Large Enterprises', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4', desc: 'Multi-location operations, advanced analytics, ERP integration'},
            ].map((uc, i) => (
              <div key={i} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={uc.icon} /></svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{uc.title}</h3>
                <p className="text-gray-600">{uc.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 7. Pricing Section */}
      <div className="py-20 bg-gradient-to-b from-green-50 to-white">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h2>
            <p className="text-xl text-gray-600">Start Free. Scale Forever.</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-3xl shadow-2xl p-12 text-white text-center">
            <div className="inline-block px-6 py-3 bg-white/20 backdrop-blur-sm rounded-full text-xl font-bold mb-6">🎉 LAUNCH OFFER</div>
            <h3 className="text-5xl font-extrabold mb-4">100% FREE</h3>
            <p className="text-2xl mb-8 text-green-100">Forever. No Catches. No Trials.</p>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="text-4xl font-bold mb-2">∞</div>
                <div className="text-lg">Unlimited Tenders</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="text-4xl font-bold mb-2">∞</div>
                <div className="text-lg">Unlimited Users</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="text-4xl font-bold mb-2">✓</div>
                <div className="text-lg">All Features</div>
              </div>
            </div>

            <button onClick={() => navigate('/register')} className="bg-white text-green-600 px-12 py-4 rounded-xl text-xl font-bold hover:bg-gray-100 shadow-2xl">
              Start Free Now →
            </button>
            <p className="mt-4 text-green-100 text-sm">No credit card required • No setup fee • Instant access</p>
          </div>
        </div>
      </div>

      {/* 8. Before/After Case Study */}
      <div className="bg-gray-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Real Results from Real Users</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {metric: 'BOQ Preparation', before: '6 Hours', after: '20 Minutes', savings: '95% Time Saved'},
              {metric: 'Tender Errors', before: '15-20 per bid', after: '0-1 per bid', savings: '98% Error Reduction'},
              {metric: 'Monthly Bids', before: '5-8 bids', after: '25-30 bids', savings: '4x More Capacity'},
            ].map((cs, i) => (
              <div key={i} className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
                <h3 className="text-2xl font-bold mb-6 text-center">{cs.metric}</h3>
                <div className="flex items-center justify-between mb-4">
                  <div className="text-center">
                    <div className="text-red-400 text-sm mb-2">❌ Before</div>
                    <div className="text-3xl font-bold">{cs.before}</div>
                  </div>
                  <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
                  <div className="text-center">
                    <div className="text-green-400 text-sm mb-2">✅ After</div>
                    <div className="text-3xl font-bold">{cs.after}</div>
                  </div>
                </div>
                <div className="text-center pt-4 border-t border-white/20">
                  <span className="inline-block px-4 py-2 bg-green-500 rounded-full font-bold">{cs.savings}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 9. FAQs */}
      <div className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
          </div>

          <div className="space-y-4">
            {[
              {q: 'Is HexaBid really 100% free?', a: 'Yes! HexaBid is completely free forever with all features. No trial periods, no hidden costs, no credit card required.'},
              {q: 'Does it integrate with GeM portal?', a: 'Yes! HexaBid auto-fetches tenders from Government e-Marketplace (GeM) and other government portals with smart categorization.'},
              {q: 'How accurate is the AI?', a: 'Our AI achieves 95%+ accuracy in tender parsing, BOQ generation, and compliance checking. All AI outputs are editable and reviewable.'},
              {q: 'Is my data secure?', a: 'Absolutely. We use bank-grade encryption, role-based access control, and secure cloud infrastructure. Your data is yours alone.'},
              {q: 'What document formats are supported?', a: 'We support all standard formats including PDF, Excel, Word, images, and scanned documents with OCR.'},
              {q: 'Can multiple team members collaborate?', a: 'Yes! Invite unlimited team members with role-based permissions (Admin, Manager, Viewer).'},
              {q: 'Do I need technical knowledge?', a: 'No! HexaBid is designed for non-technical users. If you can use email, you can use HexaBid.'},
              {q: 'What if I need help?', a: 'We provide 24/7 support via chat, email, and phone. Plus comprehensive documentation and video tutorials.'},
            ].map((faq, i) => (
              <details key={i} className="group bg-gray-50 rounded-xl p-6 hover:bg-gray-100 transition cursor-pointer">
                <summary className="font-bold text-lg text-gray-900 flex justify-between items-center">
                  {faq.q}
                  <svg className="w-5 h-5 text-gray-500 group-open:rotate-180 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                </summary>
                <p className="mt-4 text-gray-600 leading-relaxed">{faq.a}</p>
              </details>
            ))}
          </div>
        </div>
      </div>

      {/* 10. Final CTA */}
      <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-20">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-5xl font-extrabold mb-6">Ready to Win More Tenders?</h2>
          <p className="text-2xl mb-4 text-blue-100">Join thousands of tender professionals already using HexaBid</p>
          <p className="text-3xl font-bold mb-8 text-yellow-300">Start in 60 Seconds • 100% Free • No Credit Card</p>
          <button onClick={() => navigate('/register')} className="bg-white text-blue-600 px-12 py-5 rounded-xl text-2xl font-extrabold hover:bg-gray-100 shadow-2xl inline-flex items-center">
            Start Free Now
            <svg className="w-7 h-7 ml-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <img src="https://customer-assets.emergentagent.com/job_tender-master-4/artifacts/9595dbly_1%20HexaBid%20Logo%20Sm.jpg" alt="HexaBid" className="h-10 w-auto" />
                <span className="text-xl font-bold">HexaBid</span>
              </div>
              <p className="text-gray-400 text-sm mb-4">India's premier AI-powered tender management platform.</p>
              <div className="flex items-center space-x-2 mb-4">
                <span className="w-2 h-2 rounded-full bg-orange-500"></span>
                <span className="w-2 h-2 rounded-full bg-white"></span>
                <span className="w-2 h-2 rounded-full bg-green-500"></span>
                <span className="text-xs text-gray-400 ml-2">Proudly Made in India</span>
              </div>
              {/* Social Media Links */}
              {settings?.socialMediaLinks && settings.socialMediaLinks.length > 0 && (
                <div className="flex space-x-3 mt-4">
                  {settings.socialMediaLinks.map((link, idx) => (
                    <a
                      key={idx}
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-8 h-8 bg-gray-800 hover:bg-blue-600 rounded-full flex items-center justify-center transition"
                    >
                      <span className="text-sm capitalize">{link.platform.charAt(0)}</span>
                    </a>
                  ))}
                </div>
              )}
            </div>
            <div>
              <h4 className="font-semibold mb-3">Platform</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Tender Discovery</li>
                <li>AI BOQ Generator</li>
                <li>RFQ Management</li>
                <li>Document Automation</li>
                <li>Analytics & MIS</li>
                <li>ERP Modules</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Resources</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Documentation</li>
                <li>Video Tutorials</li>
                <li>Case Studies</li>
                <li>Blog</li>
                <li>API Documentation</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Contact Us</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li className="flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  {settings?.contactInfo?.phone1 || '+91 8806106575'}
                </li>
                <li className="flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  {settings?.contactInfo?.phone2 || '+91 9607500750'}
                </li>
                <li className="flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  {settings?.contactInfo?.email || 'support@cctverp.com'}
                </li>
                <li>
                  <button
                    onClick={() => window.open(`https://wa.me/${(settings?.contactInfo?.whatsappNumber || '+918806106575').replace(/[^0-9]/g, '')}`, '_blank')}
                    className="flex items-center text-green-400 hover:text-green-300"
                  >
                    <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                    </svg>
                    WhatsApp Support
                  </button>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-400 mb-4 md:mb-0">
              <p>© 2024 HexaBid. All rights reserved.</p>
              <p className="mt-1 text-xs">Created by Snxwfairies Innovations Pvt. Ltd.</p>
            </div>
            <div className="flex space-x-4 text-sm text-gray-400">
              <Link to="/help" className="hover:text-white">Help</Link>
              <Link to="/feedback" className="hover:text-white">Send Feedback</Link>
              <Link to="/privacy" className="hover:text-white">Privacy</Link>
              <Link to="/terms" className="hover:text-white">Terms</Link>
            </div>
          </div>
        </div>
      </footer>

      {/* AI Chatbot */}
      {settings?.enableChatbot && <AIChatbot />}
      
      {/* WhatsApp Button */}
      <WhatsAppButton />

      {/* Demo Modal */}
      {showDemo && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50" onClick={() => setShowDemo(false)}>
          <div className="bg-white rounded-2xl p-8 max-w-2xl w-full" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold">Watch HexaBid Demo</h3>
              <button onClick={() => setShowDemo(false)} className="text-gray-400 hover:text-gray-600">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            <div className="aspect-video bg-gray-200 rounded-lg flex items-center justify-center">
              <p className="text-gray-500">Demo video coming soon!</p>
            </div>
            <button onClick={() => navigate('/register')} className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">
              Start Using HexaBid Free →
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPage;

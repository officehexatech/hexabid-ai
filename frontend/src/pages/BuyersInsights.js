import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function BuyersInsights() {
  const [recommendations, setRecommendations] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchRecommendations();
    fetchInsights();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/buyers/recommendations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
    setLoading(false);
  };

  const fetchInsights = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/buyers/insights`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setInsights(response.data.insights);
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  const analyzeCustomKeywords = async () => {
    const keywords = prompt('Enter keywords (comma-separated):');
    if (!keywords) return;

    setAnalyzing(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/api/buyers/analyze`, {
        keywords: keywords.split(',').map(k => k.trim()),
        days: 365
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      alert(`Analysis complete! Found ${response.data.analysis.total_buyers_found} buyers`);
      fetchRecommendations();
      fetchInsights();
    } catch (error) {
      console.error('Error analyzing:', error);
      alert('Analysis failed');
    }
    setAnalyzing(false);
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Buyers Insights</h1>
          <p className="text-gray-600 mt-2">Discover potential buyers based on your profile</p>
        </div>
        <button
          onClick={analyzeCustomKeywords}
          disabled={analyzing}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {analyzing ? 'Analyzing...' : '🔍 Analyze Custom Keywords'}
        </button>
      </div>

      {/* Market Insights */}
      {insights && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Total Opportunities</p>
            <p className="text-2xl font-bold text-blue-600">{insights.total_opportunities}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Avg Tender Value</p>
            <p className="text-2xl font-bold text-green-600">₹{(insights.avg_tender_value / 100000).toFixed(2)}L</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Most Active</p>
            <p className="text-lg font-bold text-purple-600">{insights.most_active_buyer}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Best Success Rate</p>
            <p className="text-lg font-bold text-orange-600">{insights.best_success_rate_buyer || 'N/A'}</p>
          </div>
        </div>
      )}

      {/* Top Recommendations */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">🎯 Top Buyer Recommendations</h2>
        
        {loading ? (
          <p className="text-center text-gray-500 py-8">Loading recommendations...</p>
        ) : recommendations.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">No recommendations yet</p>
            <p className="text-sm text-gray-400">Complete your company profile to get personalized buyer recommendations</p>
          </div>
        ) : (
          <div className="space-y-4">
            {recommendations.map((buyer, index) => (
              <div key={index} className="border rounded-lg p-4 hover:border-blue-500 transition">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-lg">{buyer.organization_name}</h3>
                      <span className="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded">
                        {buyer.relevance_score}% Match
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 mt-3">
                      <div>
                        <p className="text-sm text-gray-600">Total Tenders Posted</p>
                        <p className="font-semibold">{buyer.total_tenders_posted}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Avg Tender Value</p>
                        <p className="font-semibold">₹{(buyer.avg_tender_value / 100000).toFixed(2)}L</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Tender Frequency</p>
                        <p className="font-semibold">{buyer.tender_frequency}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Success Rate</p>
                        <p className="font-semibold text-green-600">{buyer.success_rate_with_us}%</p>
                      </div>
                    </div>

                    <div className="mt-3">
                      <p className="text-sm text-gray-600">Categories:</p>
                      <div className="flex gap-2 mt-1 flex-wrap">
                        {buyer.preferred_categories.map((cat, idx) => (
                          <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                            {cat}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="text-gray-600">Avg Response Time:</span>
                        <span className="ml-2 font-semibold">{buyer.avg_response_time}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Peak Months:</span>
                        <span className="ml-2 font-semibold">{buyer.procurement_patterns?.peak_months.join(', ')}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recent Tenders */}
                <div className="mt-4 pt-4 border-t">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Recent Tenders:</p>
                  <div className="space-y-2">
                    {buyer.recent_tenders.slice(0, 2).map((tender, idx) => (
                      <div key={idx} className="text-sm bg-gray-50 p-2 rounded">
                        <p className="font-medium">{tender.title}</p>
                        <div className="flex justify-between text-xs text-gray-600 mt-1">
                          <span>{tender.tender_id}</span>
                          <span>₹{(tender.value / 100000).toFixed(2)}L</span>
                          <span>{tender.posted_date}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Contact Info */}
                <div className="mt-3 flex gap-4 text-sm">
                  <span className="text-blue-600">📧 {buyer.contact_info?.email}</span>
                  <span className="text-blue-600">📞 {buyer.contact_info?.phone}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default BuyersInsights;

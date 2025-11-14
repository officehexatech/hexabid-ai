import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function CompetitorAnalysis() {
  const [competitors, setCompetitors] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    fetchCompetitorAnalysis();
    fetchInsights();
  }, []);

  const fetchCompetitorAnalysis = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/competitors/analysis`, {
        params: { category: selectedCategory || undefined },
        headers: { Authorization: `Bearer ${token}` }
      });
      setCompetitors(response.data.competitors || []);
    } catch (error) {
      console.error('Error fetching competitors:', error);
    }
    setLoading(false);
  };

  const fetchInsights = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/competitors/dashboard/insights`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setInsights(response.data.insights);
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Competitor Analysis</h1>
        <p className="text-gray-600 mt-2">Track and analyze competitor bidding patterns</p>
      </div>

      {/* Insights Cards */}
      {insights && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Total Competitors</p>
            <p className="text-2xl font-bold text-blue-600">{insights.total_competitors}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Avg Market Win Rate</p>
            <p className="text-2xl font-bold text-green-600">{insights.avg_market_win_rate}%</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Avg Market Bid</p>
            <p className="text-2xl font-bold text-purple-600">₹{(insights.avg_market_bid_amount / 100000).toFixed(2)}L</p>
          </div>
        </div>
      )}

      {/* Filter */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">Category Filter</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            >
              <option value="">All Categories</option>
              <option value="IT Hardware">IT Hardware</option>
              <option value="IT Software">IT Software</option>
              <option value="Office Equipment">Office Equipment</option>
            </select>
          </div>
          <button
            onClick={fetchCompetitorAnalysis}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Apply Filter
          </button>
        </div>
      </div>

      {/* Top Performers */}
      {insights && insights.top_performers && insights.top_performers.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">🏆 Top Performers</h2>
          <div className="space-y-3">
            {insights.top_performers.map((comp, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}</span>
                  <div>
                    <p className="font-semibold">{comp.company_name}</p>
                    <p className="text-sm text-gray-600">{comp.total_bids} bids | {comp.won_bids} wins</p>
                  </div>
                </div>
                <span className="text-lg font-bold text-green-600">{comp.win_rate.toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Competitors List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold">All Competitors ({competitors.length})</h2>
        </div>
        
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading competitors...</div>
        ) : competitors.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No competitors data available</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Bids</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Won Bids</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Win Rate</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Bid Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Strategy</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {competitors.map((competitor, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-medium text-gray-900">{competitor.company_name}</p>
                        <p className="text-sm text-gray-500">{competitor.categories.join(', ')}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{competitor.total_bids}</td>
                    <td className="px-6 py-4 text-sm text-green-600 font-medium">{competitor.won_bids}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-sm rounded-full ${
                        competitor.win_rate > 50 ? 'bg-green-100 text-green-600' :
                        competitor.win_rate > 30 ? 'bg-yellow-100 text-yellow-600' :
                        'bg-red-100 text-red-600'
                      }`}>
                        {competitor.win_rate.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">₹{(competitor.avg_bid_amount / 100000).toFixed(2)}L</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-sm rounded-full ${
                        competitor.avg_bid_amount < 800000 ? 'bg-red-100 text-red-600' :
                        competitor.avg_bid_amount < 1000000 ? 'bg-yellow-100 text-yellow-600' :
                        'bg-blue-100 text-blue-600'
                      }`}>
                        {competitor.avg_bid_amount < 800000 ? 'Aggressive' :
                         competitor.avg_bid_amount < 1000000 ? 'Competitive' : 'Premium'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default CompetitorAnalysis;

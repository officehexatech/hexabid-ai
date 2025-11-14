import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function GEMIntegration() {
  const [activeTab, setActiveTab] = useState('search');
  const [searchKeywords, setSearchKeywords] = useState('');
  const [searchCategory, setSearchCategory] = useState('');
  const [tenders, setTenders] = useState([]);
  const [myBids, setMyBids] = useState([]);
  const [bidStats, setBidStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (activeTab === 'mybids') {
      fetchMyBids();
      fetchBidStats();
    }
  }, [activeTab]);

  const fetchMyBids = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/gem/bids/my-bids`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMyBids(response.data.bids || []);
    } catch (error) {
      console.error('Error fetching bids:', error);
    }
  };

  const fetchBidStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/gem/dashboard/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBidStats(response.data.stats);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const searchGEMTenders = async () => {
    if (!searchKeywords.trim()) return;
    
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/gem/tenders/search`, {
        params: { keywords: searchKeywords, category: searchCategory },
        headers: { Authorization: `Bearer ${token}` }
      });
      setTenders(response.data.tenders || []);
    } catch (error) {
      console.error('Error searching tenders:', error);
      alert('Failed to search tenders');
    }
    setLoading(false);
  };

  const trackBidStatus = async (bidId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/gem/bids/${bidId}/status`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert(`Bid Status: ${response.data.live_status.status}`);
      fetchMyBids();
    } catch (error) {
      console.error('Error tracking bid:', error);
      alert('Failed to track bid status');
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">GeM Portal Integration</h1>
        <p className="text-gray-600 mt-2">Search tenders, track bids, and analyze results from GeM portal</p>
      </div>

      {/* Stats Cards */}
      {bidStats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Total Bids</p>
            <p className="text-2xl font-bold text-blue-600">{bidStats.total_bids}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Won Bids</p>
            <p className="text-2xl font-bold text-green-600">{bidStats.won_bids}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Pending</p>
            <p className="text-2xl font-bold text-yellow-600">{bidStats.pending_bids}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-gray-600 text-sm">Win Rate</p>
            <p className="text-2xl font-bold text-purple-600">{bidStats.win_rate}%</p>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b">
          <nav className="flex">
            <button
              onClick={() => setActiveTab('search')}
              className={`px-6 py-3 font-medium ${activeTab === 'search' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
            >
              Search Tenders
            </button>
            <button
              onClick={() => setActiveTab('mybids')}
              className={`px-6 py-3 font-medium ${activeTab === 'mybids' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
            >
              My Bids
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'search' && (
            <div>
              {/* Search Form */}
              <div className="mb-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="md:col-span-2">
                    <input
                      type="text"
                      placeholder="Search keywords (e.g., IT Hardware, Laptops)"
                      value={searchKeywords}
                      onChange={(e) => setSearchKeywords(e.target.value)}
                      className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                      onKeyPress={(e) => e.key === 'Enter' && searchGEMTenders()}
                    />
                  </div>
                  <div>
                    <select
                      value={searchCategory}
                      onChange={(e) => setSearchCategory(e.target.value)}
                      className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                    >
                      <option value="">All Categories</option>
                      <option value="IT Hardware">IT Hardware</option>
                      <option value="IT Software">IT Software</option>
                      <option value="Office Equipment">Office Equipment</option>
                      <option value="Furniture">Furniture</option>
                      <option value="Medical Equipment">Medical Equipment</option>
                    </select>
                  </div>
                </div>
                <button
                  onClick={searchGEMTenders}
                  disabled={loading}
                  className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
                >
                  {loading ? 'Searching...' : 'Search GeM Tenders'}
                </button>
              </div>

              {/* Search Results */}
              {tenders.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-4">Search Results ({tenders.length})</h3>
                  <div className="space-y-4">
                    {tenders.map((tender, index) => (
                      <div key={index} className="border rounded-lg p-4 hover:border-blue-500 transition">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h4 className="font-semibold text-lg">{tender.title}</h4>
                            <p className="text-gray-600 text-sm mt-1">{tender.tender_number}</p>
                            <p className="text-gray-700 mt-2">{tender.organization}</p>
                            <div className="flex gap-4 mt-3 text-sm">
                              <span className="text-gray-600">📍 {tender.location}</span>
                              <span className="text-gray-600">📁 {tender.category}</span>
                              <span className="text-gray-600">💰 ₹{(tender.tender_value / 100000).toFixed(2)}L</span>
                            </div>
                            <div className="flex gap-4 mt-2 text-sm">
                              <span className="text-blue-600">📅 Deadline: {tender.submission_deadline}</span>
                            </div>
                          </div>
                          <span className="px-3 py-1 bg-green-100 text-green-600 rounded-full text-sm">
                            {tender.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'mybids' && (
            <div>
              <h3 className="text-lg font-semibold mb-4">My Submitted Bids</h3>
              {myBids.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No bids submitted yet</p>
              ) : (
                <div className="space-y-4">
                  {myBids.map((bid) => (
                    <div key={bid.bid_id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h4 className="font-semibold">{bid.tender_title}</h4>
                          <p className="text-gray-600 text-sm mt-1">{bid.tender_number}</p>
                          <p className="text-gray-700 mt-2">Bid Amount: ₹{(bid.bid_amount / 100000).toFixed(2)}L</p>
                          <p className="text-gray-600 text-sm mt-1">Submitted: {new Date(bid.submission_date).toLocaleDateString()}</p>
                          {bid.ranking && (
                            <p className="text-blue-600 text-sm mt-1">Rank: #{bid.ranking} of {bid.total_bidders}</p>
                          )}
                        </div>
                        <div className="flex flex-col items-end gap-2">
                          <span className={`px-3 py-1 rounded-full text-sm ${
                            bid.result_status === 'awarded' ? 'bg-green-100 text-green-600' :
                            bid.result_status === 'rejected' ? 'bg-red-100 text-red-600' :
                            'bg-yellow-100 text-yellow-600'
                          }`}>
                            {bid.status}
                          </span>
                          <button
                            onClick={() => trackBidStatus(bid.bid_id)}
                            className="px-4 py-1 text-sm bg-blue-100 text-blue-600 rounded hover:bg-blue-200"
                          >
                            Track Status
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default GEMIntegration;

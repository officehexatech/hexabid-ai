import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const CompanyProfile = () => {
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();
  const [formData, setFormData] = useState({
    companyName: '',
    industry: '',
    address: '',
    taxId: '',
    logoUrl: '',
    authorizedPersonName: '',
    authorizedPersonMobile: '',
    authorizedPersonEmail: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [existingProfile, setExistingProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get(`${API_URL}/company/profile`);
        setExistingProfile(response.data);
        setFormData(response.data);
      } catch (err) {
        if (err.response?.status !== 404) {
          console.error('Failed to fetch profile:', err);
        }
      }
    };

    if (user?.hasCompletedProfile) {
      fetchProfile();
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (existingProfile) {
        await axios.patch(`${API_URL}/company/profile`, formData);
      } else {
        await axios.post(`${API_URL}/company/profile`, formData);
      }
      await refreshUser();
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save company profile');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-8">
            <h1 className="text-3xl font-bold text-white">Company Profile</h1>
            <p className="mt-2 text-blue-100">
              {existingProfile ? 'Update your company information' : 'Complete your company profile to continue'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="px-6 py-8 space-y-6">
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Company Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.companyName}
                  onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Acme Corporation"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Industry <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.industry}
                  onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Manufacturing, IT, etc."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tax ID / GSTIN <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.taxId}
                  onChange={(e) => setFormData({ ...formData, taxId: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="29XXXXX1234X1ZX"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Address <span className="text-red-500">*</span>
                </label>
                <textarea
                  required
                  rows={3}
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Street, City, State, PIN"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Company Logo URL (Optional)
                </label>
                <input
                  type="url"
                  value={formData.logoUrl}
                  onChange={(e) => setFormData({ ...formData, logoUrl: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="https://example.com/logo.png"
                />
              </div>

              <div className="md:col-span-2 border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Authorized Person Details</h3>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.authorizedPersonName}
                  onChange={(e) => setFormData({ ...formData, authorizedPersonName: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Mobile Number <span className="text-red-500">*</span>
                </label>
                <input
                  type="tel"
                  required
                  value={formData.authorizedPersonMobile}
                  onChange={(e) => setFormData({ ...formData, authorizedPersonMobile: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="+91 1234567890"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  required
                  value={formData.authorizedPersonEmail}
                  onChange={(e) => setFormData({ ...formData, authorizedPersonEmail: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="john@example.com"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-4 pt-6 border-t">
              {existingProfile && (
                <button
                  type="button"
                  onClick={() => navigate('/dashboard')}
                  className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-semibold hover:bg-gray-50 transition"
                >
                  Cancel
                </button>
              )}
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:bg-blue-300"
              >
                {loading ? 'Saving...' : (existingProfile ? 'Update Profile' : 'Complete Profile')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CompanyProfile;

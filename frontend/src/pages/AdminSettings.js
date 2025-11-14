import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const AdminSettings = () => {
  const { user } = useAuth();
  const [settings, setSettings] = useState({
    contactInfo: {
      phone1: '+91 8806106575',
      phone2: '+91 9607500750',
      email: 'support@cctverp.com',
      whatsappNumber: '+918806106575'
    },
    socialMediaLinks: [
      { platform: 'facebook', url: 'https://facebook.com/hexabid' },
      { platform: 'twitter', url: 'https://twitter.com/hexabid' },
      { platform: 'linkedin', url: 'https://linkedin.com/company/hexabid' }
    ],
    enableChatbot: true
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API_URL}/settings/public`);
      setSettings(response.data);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    try {
      await axios.patch(`${API_URL}/settings/admin`, settings);
      setMessage('Settings updated successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Failed to update settings:', error);
      setMessage('Failed to update settings. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const addSocialLink = () => {
    setSettings({
      ...settings,
      socialMediaLinks: [...settings.socialMediaLinks, { platform: '', url: '' }]
    });
  };

  const removeSocialLink = (index) => {
    const newLinks = settings.socialMediaLinks.filter((_, i) => i !== index);
    setSettings({ ...settings, socialMediaLinks: newLinks });
  };

  const updateSocialLink = (index, field, value) => {
    const newLinks = [...settings.socialMediaLinks];
    newLinks[index] = { ...newLinks[index], [field]: value };
    setSettings({ ...settings, socialMediaLinks: newLinks });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Platform Settings</h1>
        <p className="mt-2 text-gray-600">Manage contact information, social media links, and platform features</p>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${
          message.includes('success') ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-800 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Contact Information */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Contact Information</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Phone 1 *</label>
              <input
                type="tel"
                required
                value={settings.contactInfo.phone1}
                onChange={(e) => setSettings({
                  ...settings,
                  contactInfo: { ...settings.contactInfo, phone1: e.target.value }
                })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Phone 2 *</label>
              <input
                type="tel"
                required
                value={settings.contactInfo.phone2}
                onChange={(e) => setSettings({
                  ...settings,
                  contactInfo: { ...settings.contactInfo, phone2: e.target.value }
                })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
              <input
                type="email"
                required
                value={settings.contactInfo.email}
                onChange={(e) => setSettings({
                  ...settings,
                  contactInfo: { ...settings.contactInfo, email: e.target.value }
                })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">WhatsApp Number *</label>
              <input
                type="tel"
                required
                value={settings.contactInfo.whatsappNumber}
                onChange={(e) => setSettings({
                  ...settings,
                  contactInfo: { ...settings.contactInfo, whatsappNumber: e.target.value }
                })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="+918806106575"
              />
            </div>
          </div>
        </div>

        {/* Social Media Links */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Social Media Links</h2>
            <button
              type="button"
              onClick={addSocialLink}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700"
            >
              + Add Link
            </button>
          </div>
          <div className="space-y-4">
            {settings.socialMediaLinks.map((link, index) => (
              <div key={index} className="grid md:grid-cols-12 gap-4 items-end">
                <div className="md:col-span-3">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
                  <select
                    value={link.platform}
                    onChange={(e) => updateSocialLink(index, 'platform', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select...</option>
                    <option value="facebook">Facebook</option>
                    <option value="twitter">Twitter</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="instagram">Instagram</option>
                    <option value="youtube">YouTube</option>
                  </select>
                </div>
                <div className="md:col-span-8">
                  <label className="block text-sm font-medium text-gray-700 mb-2">URL</label>
                  <input
                    type="url"
                    value={link.url}
                    onChange={(e) => updateSocialLink(index, 'url', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="https://..."
                  />
                </div>
                <div className="md:col-span-1">
                  <button
                    type="button"
                    onClick={() => removeSocialLink(index)}
                    className="w-full px-4 py-3 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 font-semibold"
                  >
                    ×
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Platform Features */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Platform Features</h2>
          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="enableChatbot"
              checked={settings.enableChatbot}
              onChange={(e) => setSettings({ ...settings, enableChatbot: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="enableChatbot" className="text-gray-700 font-medium">
              Enable AI Chatbot on Landing Page
            </label>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-blue-300 transition"
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AdminSettings;
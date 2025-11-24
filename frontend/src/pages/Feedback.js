import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const Feedback = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    category: 'feature',
    subject: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Store feedback in MongoDB
      await axios.post(`${API_URL}/feedback`, {
        ...formData,
        submittedAt: new Date().toISOString()
      });
      setSubmitted(true);
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      alert('Failed to submit feedback. Please try again or email us directly.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-3">
              <img src="https://customer-assets.emergentagent.com/job_tender-master-4/artifacts/9595dbly_1%20HexaBid%20Logo%20Sm.jpg" alt="HexaBid" className="h-10 w-auto" />
              <span className="text-2xl font-bold text-gray-900">HexaBid</span>
            </Link>
            <Link to="/" className="text-blue-600 hover:text-blue-700 font-semibold">← Back to Home</Link>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Send Us Your Feedback</h1>
          <p className="text-xl text-gray-600">We value your input and continuously improve HexaBid based on your suggestions.</p>
        </div>

        {submitted ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Thank You!</h2>
            <p className="text-gray-600 mb-6">Your feedback has been submitted successfully. We'll review it and get back to you if needed.</p>
            <button
              onClick={() => setSubmitted(false)}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
            >
              Submit Another Feedback
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-8 space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Your Name *</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email Address *</label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="john@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category *</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="feature">Feature Request</option>
                <option value="bug">Bug Report</option>
                <option value="improvement">Improvement Suggestion</option>
                <option value="general">General Feedback</option>
                <option value="complaint">Complaint</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Subject *</label>
              <input
                type="text"
                required
                value={formData.subject}
                onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Brief description of your feedback"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Message *</label>
              <textarea
                required
                rows={6}
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Please provide detailed feedback..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 transition disabled:bg-blue-300"
            >
              {loading ? 'Submitting...' : 'Submit Feedback'}
            </button>
          </form>
        )}

        {/* Alternative Contact */}
        <div className="mt-8 text-center">
          <p className="text-gray-600 mb-4">Prefer to contact us directly?</p>
          <div className="flex justify-center space-x-4">
            <a href="mailto:support@hexabid.in" className="text-blue-600 hover:text-blue-700 font-semibold">Email Us</a>
            <span className="text-gray-400">|</span>
            <button onClick={() => window.open('https://wa.me/918806106575', '_blank')} className="text-green-600 hover:text-green-700 font-semibold">WhatsApp</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Feedback;
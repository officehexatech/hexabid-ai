import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function EmailClient() {
  const [activeTab, setActiveTab] = useState('inbox');
  const [emails, setEmails] = useState([]);
  const [composing, setComposing] = useState(false);
  const [composeData, setComposeData] = useState({ to: '', subject: '', body: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEmails(activeTab);
  }, [activeTab]);

  const fetchEmails = async (folder) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/email/${folder}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEmails(response.data.emails || []);
    } catch (error) {
      console.error('Error fetching emails:', error);
    }
    setLoading(false);
  };

  const sendEmail = async () => {
    if (!composeData.to || !composeData.subject || !composeData.body) {
      alert('Please fill all fields');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_URL}/api/email/send`, {
        to: [composeData.to],
        subject: composeData.subject,
        body: composeData.body,
        attachments: []
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      alert('Email sent successfully (Mock Mode)');
      setComposing(false);
      setComposeData({ to: '', subject: '', body: '' });
    } catch (error) {
      console.error('Error sending email:', error);
      alert('Failed to send email');
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Email Client</h1>
          <p className="text-gray-600 mt-2">Manage your tender-related emails (Mock Mode)</p>
        </div>
        <button
          onClick={() => setComposing(!composing)}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          ✉️ Compose
        </button>
      </div>

      {/* Compose Email Modal */}
      {composing && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Compose Email</h2>
          <div className="space-y-4">
            <input
              type="email"
              placeholder="To: recipient@example.com"
              value={composeData.to}
              onChange={(e) => setComposeData({...composeData, to: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
            <input
              type="text"
              placeholder="Subject"
              value={composeData.subject}
              onChange={(e) => setComposeData({...composeData, subject: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
            <textarea
              placeholder="Email body..."
              value={composeData.body}
              onChange={(e) => setComposeData({...composeData, body: e.target.value})}
              rows="6"
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            ></textarea>
            <div className="flex gap-3">
              <button
                onClick={sendEmail}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Send
              </button>
              <button
                onClick={() => setComposing(false)}
                className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Email Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b">
          <nav className="flex">
            <button
              onClick={() => setActiveTab('inbox')}
              className={`px-6 py-3 font-medium ${activeTab === 'inbox' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
            >
              📥 Inbox
            </button>
            <button
              onClick={() => setActiveTab('sent')}
              className={`px-6 py-3 font-medium ${activeTab === 'sent' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
            >
              📤 Sent
            </button>
          </nav>
        </div>

        <div className="p-6">
          {loading ? (
            <p className="text-center text-gray-500 py-8">Loading emails...</p>
          ) : emails.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No emails</p>
          ) : (
            <div className="space-y-3">
              {emails.map((email, index) => (
                <div key={index} className={`p-4 border rounded-lg hover:border-blue-500 transition ${
                  email.is_read ? 'bg-gray-50' : 'bg-white border-l-4 border-l-blue-500'
                }`}>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-semibold">{email.from}</p>
                        {!email.is_read && <span className="text-xs bg-blue-500 text-white px-2 py-1 rounded">New</span>}
                        {email.has_attachments && <span className="text-xs">📎</span>}
                      </div>
                      <p className="font-medium mt-1">{email.subject}</p>
                      <p className="text-sm text-gray-600 mt-1">{email.snippet}</p>
                    </div>
                    <p className="text-xs text-gray-500">{new Date(email.received_at).toLocaleDateString()}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Mock Mode Notice */}
      <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-sm text-yellow-800">
          ℹ️ <strong>Mock Mode:</strong> Email client is running in mock mode. Configure Gmail API credentials to enable real email functionality.
        </p>
      </div>
    </div>
  );
}

export default EmailClient;

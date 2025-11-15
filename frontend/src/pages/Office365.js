import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function Office365() {
  const [documents, setDocuments] = useState([]);
  const [creating, setCreating] = useState(false);
  const [newDoc, setNewDoc] = useState({ type: 'word', title: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/office365/documents/list`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDocuments(response.data.documents || []);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
    setLoading(false);
  };

  const createDocument = async () => {
    if (!newDoc.title) {
      alert('Please enter document title');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_URL}/api/office365/documents/create`, {
        document_type: newDoc.type,
        title: newDoc.title
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      alert('Document created successfully (Mock Mode)');
      setCreating(false);
      setNewDoc({ type: 'word', title: '' });
      fetchDocuments();
    } catch (error) {
      console.error('Error creating document:', error);
      alert('Failed to create document');
    }
  };

  const getDocIcon = (type) => {
    switch(type) {
      case 'word': return '📄';
      case 'excel': return '📊';
      case 'powerpoint': return '📽️';
      case 'pdf': return '📕';
      default: return '📁';
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Office 365</h1>
          <p className="text-gray-600 mt-2">Create and manage documents (Mock Mode)</p>
        </div>
        <button
          onClick={() => setCreating(!creating)}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          ➕ New Document
        </button>
      </div>

      {/* Create Document Modal */}
      {creating && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Create New Document</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Document Type</label>
              <select
                value={newDoc.type}
                onChange={(e) => setNewDoc({...newDoc, type: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              >
                <option value="word">Word Document</option>
                <option value="excel">Excel Spreadsheet</option>
                <option value="powerpoint">PowerPoint Presentation</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Document Title</label>
              <input
                type="text"
                placeholder="Enter document title"
                value={newDoc.title}
                onChange={(e) => setNewDoc({...newDoc, title: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
            <div className="flex gap-3">
              <button
                onClick={createDocument}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Create
              </button>
              <button
                onClick={() => setCreating(false)}
                className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Documents Grid */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">OneDrive Documents</h2>
        
        {loading ? (
          <p className="text-center text-gray-500 py-8">Loading documents...</p>
        ) : documents.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No documents yet</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {documents.map((doc, index) => (
              <div key={index} className="border rounded-lg p-4 hover:border-blue-500 hover:shadow-md transition">
                <div className="flex items-start gap-3">
                  <div className="text-4xl">{getDocIcon(doc.type)}</div>
                  <div className="flex-1">
                    <p className="font-semibold">{doc.title}</p>
                    <p className="text-sm text-gray-600 mt-1">{doc.type.toUpperCase()}</p>
                    <p className="text-xs text-gray-500 mt-1">{doc.size}</p>
                    <p className="text-xs text-gray-500">Modified: {new Date(doc.modified_at).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="mt-3 flex gap-2">
                  <button className="flex-1 px-3 py-1 text-sm bg-blue-100 text-blue-600 rounded hover:bg-blue-200">
                    Open
                  </button>
                  <button className="flex-1 px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
                    Share
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Mock Mode Notice */}
      <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-sm text-yellow-800">
          ℹ️ <strong>Mock Mode:</strong> Office 365 integration is running in mock mode. Configure Microsoft 365 API credentials to enable real document editing and OneDrive integration.
        </p>
      </div>
    </div>
  );
}

export default Office365;

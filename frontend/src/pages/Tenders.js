import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const Tenders = () => {
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTender, setEditingTender] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  
  const [formData, setFormData] = useState({
    tenderNumber: '',
    title: '',
    description: '',
    source: 'manual',
    organization: '',
    department: '',
    category: '',
    location: '',
    publishDate: '',
    submissionDeadline: '',
    tenderValue: '',
    emdAmount: '',
    documentUrl: '',
    notes: '',
    tags: []
  });

  useEffect(() => {
    fetchTenders();
  }, [searchTerm, filterStatus]);

  const fetchTenders = async () => {
    try {
      const token = localStorage.getItem('token');
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (filterStatus) params.status = filterStatus;
      
      const response = await axios.get(`${API_URL}/tenders`, {
        headers: { Authorization: `Bearer ${token}` },
        params
      });
      setTenders(response.data.data);
    } catch (error) {
      console.error('Failed to fetch tenders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const payload = {
        ...formData,
        tenderValue: formData.tenderValue ? parseFloat(formData.tenderValue) : null,
        emdAmount: formData.emdAmount ? parseFloat(formData.emdAmount) : null,
        tags: formData.tags.length > 0 ? formData.tags : []
      };

      if (editingTender) {
        await axios.patch(`${API_URL}/tenders/${editingTender.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post(`${API_URL}/tenders`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      
      setShowModal(false);
      resetForm();
      fetchTenders();
    } catch (error) {
      console.error('Failed to save tender:', error);
      alert('Failed to save tender: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleEdit = (tender) => {
    setEditingTender(tender);
    setFormData({
      tenderNumber: tender.tenderNumber,
      title: tender.title,
      description: tender.description || '',
      source: tender.source || 'manual',
      organization: tender.organization,
      department: tender.department || '',
      category: tender.category || '',
      location: tender.location || '',
      publishDate: tender.publishDate ? tender.publishDate.split('T')[0] : '',
      submissionDeadline: tender.submissionDeadline ? tender.submissionDeadline.split('T')[0] : '',
      tenderValue: tender.tenderValue || '',
      emdAmount: tender.emdAmount || '',
      documentUrl: tender.documentUrl || '',
      notes: tender.notes || '',
      tags: tender.tags || []
    });
    setShowModal(true);
  };

  const handleDelete = async (tenderId) => {
    if (!window.confirm('Are you sure you want to delete this tender?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/tenders/${tenderId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchTenders();
    } catch (error) {
      console.error('Failed to delete tender:', error);
      alert('Failed to delete tender');
    }
  };

  const handleStatusChange = async (tenderId, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`${API_URL}/tenders/${tenderId}`, 
        { status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchTenders();
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      tenderNumber: '',
      title: '',
      description: '',
      source: 'manual',
      organization: '',
      department: '',
      category: '',
      location: '',
      publishDate: '',
      submissionDeadline: '',
      tenderValue: '',
      emdAmount: '',
      documentUrl: '',
      notes: '',
      tags: []
    });
    setEditingTender(null);
  };

  const getStatusBadge = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      in_progress: 'bg-yellow-100 text-yellow-800',
      submitted: 'bg-purple-100 text-purple-800',
      won: 'bg-green-100 text-green-800',
      lost: 'bg-red-100 text-red-800',
      archived: 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tender Management</h1>
          <p className="mt-2 text-gray-600">Manage and track all your tenders</p>
        </div>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          + Add Tender
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search tenders..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Status</option>
          <option value="new">New</option>
          <option value="in_progress">In Progress</option>
          <option value="submitted">Submitted</option>
          <option value="won">Won</option>
          <option value="lost">Lost</option>
          <option value="archived">Archived</option>
        </select>
      </div>

      {/* Tenders Table */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tender Number</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Organization</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Deadline</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr><td colSpan="7" className="text-center py-8">Loading...</td></tr>
            ) : tenders.length === 0 ? (
              <tr><td colSpan="7" className="text-center py-8">No tenders found</td></tr>
            ) : (
              tenders.map((tender) => (
                <tr key={tender.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">{tender.tenderNumber}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{tender.title}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{tender.organization}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {tender.tenderValue ? `₹${tender.tenderValue.toLocaleString()}` : '-'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {new Date(tender.submissionDeadline).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4">
                    <select
                      value={tender.status}
                      onChange={(e) => handleStatusChange(tender.id, e.target.value)}
                      className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusBadge(tender.status)}`}
                    >
                      <option value="new">New</option>
                      <option value="in_progress">In Progress</option>
                      <option value="submitted">Submitted</option>
                      <option value="won">Won</option>
                      <option value="lost">Lost</option>
                      <option value="archived">Archived</option>
                    </select>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <button
                      onClick={() => handleEdit(tender)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(tender.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-4">{editingTender ? 'Edit Tender' : 'Add New Tender'}</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Tender Number *</label>
                    <input
                      type="text"
                      required
                      value={formData.tenderNumber}
                      onChange={(e) => setFormData({...formData, tenderNumber: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Source</label>
                    <select
                      value={formData.source}
                      onChange={(e) => setFormData({...formData, source: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="gem">GeM Portal</option>
                      <option value="cppp">CPPP</option>
                      <option value="eprocure">eProcure</option>
                      <option value="manual">Manual Entry</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Title *</label>
                  <input
                    type="text"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    rows="3"
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Organization *</label>
                    <input
                      type="text"
                      required
                      value={formData.organization}
                      onChange={(e) => setFormData({...formData, organization: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Department</label>
                    <input
                      type="text"
                      value={formData.department}
                      onChange={(e) => setFormData({...formData, department: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Category</label>
                    <input
                      type="text"
                      value={formData.category}
                      onChange={(e) => setFormData({...formData, category: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Location</label>
                    <input
                      type="text"
                      value={formData.location}
                      onChange={(e) => setFormData({...formData, location: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Publish Date</label>
                    <input
                      type="date"
                      value={formData.publishDate}
                      onChange={(e) => setFormData({...formData, publishDate: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Submission Deadline *</label>
                    <input
                      type="date"
                      required
                      value={formData.submissionDeadline}
                      onChange={(e) => setFormData({...formData, submissionDeadline: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Tender Value (₹)</label>
                    <input
                      type="number"
                      value={formData.tenderValue}
                      onChange={(e) => setFormData({...formData, tenderValue: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">EMD Amount (₹)</label>
                    <input
                      type="number"
                      value={formData.emdAmount}
                      onChange={(e) => setFormData({...formData, emdAmount: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Document URL</label>
                  <input
                    type="url"
                    value={formData.documentUrl}
                    onChange={(e) => setFormData({...formData, documentUrl: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Notes</label>
                  <textarea
                    rows="2"
                    value={formData.notes}
                    onChange={(e) => setFormData({...formData, notes: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => { setShowModal(false); resetForm(); }}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    {editingTender ? 'Update' : 'Create'} Tender
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tenders;

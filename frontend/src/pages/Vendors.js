import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const Vendors = () => {
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingVendor, setEditingVendor] = useState(null);
  const [search, setSearch] = useState('');
  const [formData, setFormData] = useState({
    companyName: '',
    vendorType: '',
    primaryContactName: '',
    primaryContactEmail: '',
    primaryContactPhone: '',
    address: '',
    city: '',
    state: '',
    pincode: '',
    gstin: '',
    pan: '',
    website: '',
    paymentTerms: '',
    categories: [],
    tags: [],
    notes: ''
  });

  useEffect(() => {
    fetchVendors();
  }, [search]);

  const fetchVendors = async () => {
    try {
      const response = await axios.get(`${API_URL}/vendors`, {
        params: { search, limit: 50 }
      });
      setVendors(response.data.data);
    } catch (error) {
      console.error('Failed to fetch vendors:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingVendor) {
        await axios.patch(`${API_URL}/vendors/${editingVendor.id}`, formData);
      } else {
        await axios.post(`${API_URL}/vendors`, formData);
      }
      setShowModal(false);
      resetForm();
      fetchVendors();
    } catch (error) {
      console.error('Failed to save vendor:', error);
      alert('Failed to save vendor. Please try again.');
    }
  };

  const handleEdit = (vendor) => {
    setEditingVendor(vendor);
    setFormData(vendor);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this vendor?')) {
      try {
        await axios.delete(`${API_URL}/vendors/${id}`);
        fetchVendors();
      } catch (error) {
        console.error('Failed to delete vendor:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      companyName: '', vendorType: '', primaryContactName: '',
      primaryContactEmail: '', primaryContactPhone: '', address: '',
      city: '', state: '', pincode: '', gstin: '', pan: '', website: '',
      paymentTerms: '', categories: [], tags: [], notes: ''
    });
    setEditingVendor(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Vendors</h1>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700"
        >
          + Add Vendor
        </button>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b">
          <input
            type="text"
            placeholder="Search vendors..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">GSTIN</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                <tr><td colSpan="5" className="text-center py-4">Loading...</td></tr>
              ) : vendors.length === 0 ? (
                <tr><td colSpan="5" className="text-center py-4 text-gray-500">No vendors found</td></tr>
              ) : (
                vendors.map((vendor) => (
                  <tr key={vendor.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{vendor.companyName}</div>
                      {vendor.vendorType && <div className="text-sm text-gray-500">{vendor.vendorType}</div>}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">{vendor.primaryContactName}</div>
                      <div className="text-sm text-gray-500">{vendor.primaryContactEmail}</div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{vendor.city}, {vendor.state}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{vendor.gstin || '-'}</td>
                    <td className="px-6 py-4 text-right text-sm font-medium">
                      <button onClick={() => handleEdit(vendor)} className="text-blue-600 hover:text-blue-900 mr-4">Edit</button>
                      <button onClick={() => handleDelete(vendor.id)} className="text-red-600 hover:text-red-900">Delete</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-screen overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-4">{editingVendor ? 'Edit Vendor' : 'Add Vendor'}</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <label className="block text-sm font-medium mb-1">Company Name *</label>
                    <input type="text" required value={formData.companyName} onChange={(e) => setFormData({...formData, companyName: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Contact Name</label>
                    <input type="text" value={formData.primaryContactName} onChange={(e) => setFormData({...formData, primaryContactName: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Contact Email</label>
                    <input type="email" value={formData.primaryContactEmail} onChange={(e) => setFormData({...formData, primaryContactEmail: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Contact Phone</label>
                    <input type="tel" value={formData.primaryContactPhone} onChange={(e) => setFormData({...formData, primaryContactPhone: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">GSTIN</label>
                    <input type="text" value={formData.gstin} onChange={(e) => setFormData({...formData, gstin: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium mb-1">Address</label>
                    <textarea rows="2" value={formData.address} onChange={(e) => setFormData({...formData, address: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">City</label>
                    <input type="text" value={formData.city} onChange={(e) => setFormData({...formData, city: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">State</label>
                    <input type="text" value={formData.state} onChange={(e) => setFormData({...formData, state: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button type="button" onClick={() => { setShowModal(false); resetForm(); }} className="px-4 py-2 border rounded-lg">Cancel</button>
                  <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Save</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Vendors;

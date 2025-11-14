import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const RFQ = () => {
  const [rfqs, setRfqs] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    rfqNumber: '',
    title: '',
    description: '',
    vendorIds: [],
    lineItems: [{ itemName: '', description: '', quantity: 1, unit: 'pcs', specifications: '' }],
    dueDate: '',
    deliveryLocation: '',
    paymentTerms: '',
    notes: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [rfqsRes, vendorsRes] = await Promise.all([
        axios.get(`${API_URL}/rfq`),
        axios.get(`${API_URL}/vendors?limit=100`)
      ]);
      setRfqs(rfqsRes.data.data);
      setVendors(vendorsRes.data.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/rfq`, formData);
      setShowModal(false);
      resetForm();
      fetchData();
    } catch (error) {
      console.error('Failed to create RFQ:', error);
      alert('Failed to create RFQ. Please try again.');
    }
  };

  const addLineItem = () => {
    setFormData({
      ...formData,
      lineItems: [...formData.lineItems, { itemName: '', description: '', quantity: 1, unit: 'pcs', specifications: '' }]
    });
  };

  const removeLineItem = (index) => {
    const newItems = formData.lineItems.filter((_, i) => i !== index);
    setFormData({ ...formData, lineItems: newItems });
  };

  const updateLineItem = (index, field, value) => {
    const newItems = [...formData.lineItems];
    newItems[index] = { ...newItems[index], [field]: value };
    setFormData({ ...formData, lineItems: newItems });
  };

  const resetForm = () => {
    setFormData({
      rfqNumber: '',
      title: '',
      description: '',
      vendorIds: [],
      lineItems: [{ itemName: '', description: '', quantity: 1, unit: 'pcs', specifications: '' }],
      dueDate: '',
      deliveryLocation: '',
      paymentTerms: '',
      notes: ''
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Request for Quotation (RFQ)</h1>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700"
        >
          + Create RFQ
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">RFQ Number</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendors</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr><td colSpan="5" className="text-center py-4">Loading...</td></tr>
            ) : rfqs.length === 0 ? (
              <tr><td colSpan="5" className="text-center py-4 text-gray-500">No RFQs found</td></tr>
            ) : (
              rfqs.map((rfq) => (
                <tr key={rfq.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">{rfq.rfqNumber}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{rfq.title}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{rfq.vendorIds.length} vendors</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{new Date(rfq.dueDate).toLocaleDateString()}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs rounded-full ${rfq.status === 'sent' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {rfq.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-screen overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-4">Create RFQ</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">RFQ Number *</label>
                    <input type="text" required value={formData.rfqNumber} onChange={(e) => setFormData({...formData, rfqNumber: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Due Date *</label>
                    <input type="datetime-local" required value={formData.dueDate} onChange={(e) => setFormData({...formData, dueDate: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium mb-1">Title *</label>
                    <input type="text" required value={formData.title} onChange={(e) => setFormData({...formData, title: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium mb-1">Description</label>
                    <textarea rows="2" value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} className="w-full px-3 py-2 border rounded-lg" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium mb-1">Select Vendors *</label>
                    <select multiple size="5" required value={formData.vendorIds} onChange={(e) => setFormData({...formData, vendorIds: Array.from(e.target.selectedOptions, option => option.value)})} className="w-full px-3 py-2 border rounded-lg">
                      {vendors.map(v => <option key={v.id} value={v.id}>{v.companyName}</option>)}
                    </select>
                    <p className="text-xs text-gray-500 mt-1">Hold Ctrl/Cmd to select multiple vendors</p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-semibold">Line Items</h3>
                    <button type="button" onClick={addLineItem} className="text-blue-600 text-sm">+ Add Item</button>
                  </div>
                  {formData.lineItems.map((item, idx) => (
                    <div key={idx} className="grid grid-cols-12 gap-2 mb-2">
                      <input type="text" placeholder="Item name" required value={item.itemName} onChange={(e) => updateLineItem(idx, 'itemName', e.target.value)} className="col-span-4 px-2 py-1 border rounded text-sm" />
                      <input type="number" placeholder="Qty" required value={item.quantity} onChange={(e) => updateLineItem(idx, 'quantity', e.target.value)} className="col-span-2 px-2 py-1 border rounded text-sm" />
                      <input type="text" placeholder="Unit" required value={item.unit} onChange={(e) => updateLineItem(idx, 'unit', e.target.value)} className="col-span-2 px-2 py-1 border rounded text-sm" />
                      <input type="text" placeholder="Specifications" value={item.specifications} onChange={(e) => updateLineItem(idx, 'specifications', e.target.value)} className="col-span-3 px-2 py-1 border rounded text-sm" />
                      <button type="button" onClick={() => removeLineItem(idx)} className="col-span-1 text-red-600 text-sm">×</button>
                    </div>
                  ))}
                </div>

                <div className="flex justify-end space-x-3 mt-6">
                  <button type="button" onClick={() => { setShowModal(false); resetForm(); }} className="px-4 py-2 border rounded-lg">Cancel</button>
                  <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Create RFQ</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RFQ;

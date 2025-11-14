import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const BOQManagement = () => {
  const [boqs, setBoqs] = useState([]);
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingBoq, setEditingBoq] = useState(null);
  const [selectedTenderId, setSelectedTenderId] = useState('');
  
  const [formData, setFormData] = useState({
    tenderId: '',
    boqNumber: '',
    title: '',
    lineItems: [],
    totalEstimatedValue: 0,
    totalOurValue: 0,
    marginPercentage: 0,
    notes: ''
  });

  const [lineItem, setLineItem] = useState({
    itemNumber: '',
    description: '',
    specification: '',
    quantity: '',
    unit: '',
    estimatedRate: '',
    ourRate: '',
    remarks: ''
  });

  useEffect(() => {
    fetchTenders();
  }, []);

  useEffect(() => {
    if (selectedTenderId) {
      fetchBoqsByTender(selectedTenderId);
    }
  }, [selectedTenderId]);

  const fetchTenders = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/tenders?limit=100`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTenders(response.data.data);
      if (response.data.data.length > 0) {
        setSelectedTenderId(response.data.data[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch tenders:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchBoqsByTender = async (tenderId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/boq/tender/${tenderId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBoqs(response.data.data);
    } catch (error) {
      console.error('Failed to fetch BOQs:', error);
    }
  };

  const addLineItem = () => {
    if (!lineItem.itemNumber || !lineItem.description || !lineItem.quantity) {
      alert('Please fill required fields: Item Number, Description, Quantity');
      return;
    }

    const qty = parseFloat(lineItem.quantity) || 0;
    const estRate = parseFloat(lineItem.estimatedRate) || 0;
    const ourRate = parseFloat(lineItem.ourRate) || 0;
    
    const newLineItem = {
      ...lineItem,
      quantity: qty,
      estimatedRate: estRate,
      ourRate: ourRate,
      totalAmount: qty * ourRate
    };

    setFormData({
      ...formData,
      lineItems: [...formData.lineItems, newLineItem]
    });

    // Reset line item form
    setLineItem({
      itemNumber: '',
      description: '',
      specification: '',
      quantity: '',
      unit: '',
      estimatedRate: '',
      ourRate: '',
      remarks: ''
    });
  };

  const removeLineItem = (index) => {
    const newLineItems = formData.lineItems.filter((_, i) => i !== index);
    setFormData({ ...formData, lineItems: newLineItems });
  };

  const calculateTotals = () => {
    let totalEst = 0;
    let totalOur = 0;
    
    formData.lineItems.forEach(item => {
      totalEst += (item.quantity * (item.estimatedRate || 0));
      totalOur += (item.quantity * (item.ourRate || 0));
    });

    const margin = totalEst > 0 ? ((totalOur - totalEst) / totalEst * 100) : 0;

    return { totalEst, totalOur, margin };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.lineItems.length === 0) {
      alert('Please add at least one line item');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const totals = calculateTotals();
      
      const payload = {
        ...formData,
        tenderId: formData.tenderId || selectedTenderId,
        totalEstimatedValue: totals.totalEst,
        totalOurValue: totals.totalOur,
        marginPercentage: totals.margin
      };

      if (editingBoq) {
        await axios.patch(`${API_URL}/boq/${editingBoq.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post(`${API_URL}/boq`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      
      setShowModal(false);
      resetForm();
      fetchBoqsByTender(selectedTenderId);
    } catch (error) {
      console.error('Failed to save BOQ:', error);
      alert('Failed to save BOQ: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleEdit = (boq) => {
    setEditingBoq(boq);
    setFormData({
      tenderId: boq.tenderId,
      boqNumber: boq.boqNumber,
      title: boq.title,
      lineItems: boq.lineItems,
      totalEstimatedValue: boq.totalEstimatedValue,
      totalOurValue: boq.totalOurValue,
      marginPercentage: boq.marginPercentage,
      notes: boq.notes || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (boqId) => {
    if (!window.confirm('Are you sure you want to delete this BOQ?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/boq/${boqId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchBoqsByTender(selectedTenderId);
    } catch (error) {
      console.error('Failed to delete BOQ:', error);
      alert('Failed to delete BOQ');
    }
  };

  const resetForm = () => {
    setFormData({
      tenderId: '',
      boqNumber: '',
      title: '',
      lineItems: [],
      totalEstimatedValue: 0,
      totalOurValue: 0,
      marginPercentage: 0,
      notes: ''
    });
    setEditingBoq(null);
  };

  const totals = formData.lineItems.length > 0 ? calculateTotals() : { totalEst: 0, totalOur: 0, margin: 0 };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">BOQ Management</h1>
          <p className="mt-2 text-gray-600">Bill of Quantities & Costing</p>
        </div>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          + Create BOQ
        </button>
      </div>

      {/* Tender Filter */}
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Tender</label>
        <select
          value={selectedTenderId}
          onChange={(e) => setSelectedTenderId(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          {tenders.map((tender) => (
            <option key={tender.id} value={tender.id}>
              {tender.tenderNumber} - {tender.title}
            </option>
          ))}
        </select>
      </div>

      {/* BOQs List */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">BOQ Number</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Items</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                <tr><td colSpan="6" className="text-center py-8">Loading...</td></tr>
              ) : boqs.length === 0 ? (
                <tr><td colSpan="6" className="text-center py-8">No BOQs found for this tender</td></tr>
              ) : (
                boqs.map((boq) => (
                  <tr key={boq.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">{boq.boqNumber}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{boq.title}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{boq.lineItems.length} items</td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      ₹{(boq.totalOurValue || 0).toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        boq.status === 'approved' ? 'bg-green-100 text-green-800' :
                        boq.status === 'submitted' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {boq.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <button
                        onClick={() => handleEdit(boq)}
                        className="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(boq.id)}
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
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-4">{editingBoq ? 'Edit BOQ' : 'Create New BOQ'}</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">BOQ Number *</label>
                    <input
                      type="text"
                      required
                      value={formData.boqNumber}
                      onChange={(e) => setFormData({...formData, boqNumber: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
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
                </div>

                {/* Line Items Section */}
                <div className="border-t pt-4">
                  <h3 className="text-lg font-semibold mb-3">Line Items</h3>
                  
                  {/* Add Line Item Form */}
                  <div className="bg-gray-50 p-4 rounded-lg mb-4">
                    <div className="grid grid-cols-4 gap-3">
                      <input
                        type="text"
                        placeholder="Item Number *"
                        value={lineItem.itemNumber}
                        onChange={(e) => setLineItem({...lineItem, itemNumber: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="text"
                        placeholder="Description *"
                        value={lineItem.description}
                        onChange={(e) => setLineItem({...lineItem, description: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="number"
                        placeholder="Quantity *"
                        value={lineItem.quantity}
                        onChange={(e) => setLineItem({...lineItem, quantity: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="text"
                        placeholder="Unit"
                        value={lineItem.unit}
                        onChange={(e) => setLineItem({...lineItem, unit: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="number"
                        placeholder="Est. Rate"
                        value={lineItem.estimatedRate}
                        onChange={(e) => setLineItem({...lineItem, estimatedRate: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="number"
                        placeholder="Our Rate"
                        value={lineItem.ourRate}
                        onChange={(e) => setLineItem({...lineItem, ourRate: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="text"
                        placeholder="Specification"
                        value={lineItem.specification}
                        onChange={(e) => setLineItem({...lineItem, specification: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <button
                        type="button"
                        onClick={addLineItem}
                        className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                      >
                        Add Item
                      </button>
                    </div>
                  </div>

                  {/* Line Items Table */}
                  {formData.lineItems.length > 0 && (
                    <div className="overflow-x-auto mb-4">
                      <table className="min-w-full border border-gray-200">
                        <thead className="bg-gray-100">
                          <tr>
                            <th className="px-3 py-2 text-left text-xs">Item #</th>
                            <th className="px-3 py-2 text-left text-xs">Description</th>
                            <th className="px-3 py-2 text-left text-xs">Qty</th>
                            <th className="px-3 py-2 text-left text-xs">Unit</th>
                            <th className="px-3 py-2 text-left text-xs">Est. Rate</th>
                            <th className="px-3 py-2 text-left text-xs">Our Rate</th>
                            <th className="px-3 py-2 text-left text-xs">Amount</th>
                            <th className="px-3 py-2 text-left text-xs">Action</th>
                          </tr>
                        </thead>
                        <tbody>
                          {formData.lineItems.map((item, index) => (
                            <tr key={index} className="border-t">
                              <td className="px-3 py-2 text-sm">{item.itemNumber}</td>
                              <td className="px-3 py-2 text-sm">{item.description}</td>
                              <td className="px-3 py-2 text-sm">{item.quantity}</td>
                              <td className="px-3 py-2 text-sm">{item.unit}</td>
                              <td className="px-3 py-2 text-sm">₹{item.estimatedRate || 0}</td>
                              <td className="px-3 py-2 text-sm">₹{item.ourRate || 0}</td>
                              <td className="px-3 py-2 text-sm">₹{item.totalAmount || 0}</td>
                              <td className="px-3 py-2 text-sm">
                                <button
                                  type="button"
                                  onClick={() => removeLineItem(index)}
                                  className="text-red-600 hover:text-red-900"
                                >
                                  Remove
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}

                  {/* Totals */}
                  {formData.lineItems.length > 0 && (
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="grid grid-cols-3 gap-4 text-center">
                        <div>
                          <div className="text-sm text-gray-600">Total Estimated</div>
                          <div className="text-xl font-bold text-gray-900">₹{totals.totalEst.toLocaleString()}</div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-600">Our Total</div>
                          <div className="text-xl font-bold text-blue-600">₹{totals.totalOur.toLocaleString()}</div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-600">Margin</div>
                          <div className="text-xl font-bold text-green-600">{totals.margin.toFixed(2)}%</div>
                        </div>
                      </div>
                    </div>
                  )}
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
                    {editingBoq ? 'Update' : 'Create'} BOQ
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

export default BOQManagement;
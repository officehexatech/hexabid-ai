import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  
  const [formData, setFormData] = useState({
    productCode: '',
    productName: '',
    category: 'hardware',
    brand: '',
    model: '',
    unit: 'pcs',
    unitPrice: '',
    oemVendorId: '',
    leadTimeDays: '',
    warrantyMonths: '',
    description: '',
    imageUrl: '',
    datasheet: ''
  });

  useEffect(() => {
    fetchProducts();
  }, [searchTerm, filterCategory]);

  const fetchProducts = async () => {
    try {
      const token = localStorage.getItem('token');
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (filterCategory) params.category = filterCategory;
      
      const response = await axios.get(`${API_URL}/products`, {
        headers: { Authorization: `Bearer ${token}` },
        params
      });
      setProducts(response.data.data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
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
        unitPrice: formData.unitPrice ? parseFloat(formData.unitPrice) : null,
        leadTimeDays: formData.leadTimeDays ? parseInt(formData.leadTimeDays) : null,
        warrantyMonths: formData.warrantyMonths ? parseInt(formData.warrantyMonths) : null,
        specifications: {}
      };

      if (editingProduct) {
        await axios.patch(`${API_URL}/products/${editingProduct.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post(`${API_URL}/products`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      
      setShowModal(false);
      resetForm();
      fetchProducts();
    } catch (error) {
      console.error('Failed to save product:', error);
      alert('Failed to save product: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setFormData({
      productCode: product.productCode,
      productName: product.productName,
      category: product.category,
      brand: product.brand,
      model: product.model || '',
      unit: product.unit || 'pcs',
      unitPrice: product.unitPrice || '',
      oemVendorId: product.oemVendorId || '',
      leadTimeDays: product.leadTimeDays || '',
      warrantyMonths: product.warrantyMonths || '',
      description: product.description || '',
      imageUrl: product.imageUrl || '',
      datasheet: product.datasheet || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/products/${productId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchProducts();
    } catch (error) {
      console.error('Failed to delete product:', error);
      alert('Failed to delete product');
    }
  };

  const resetForm = () => {
    setFormData({
      productCode: '',
      productName: '',
      category: 'hardware',
      brand: '',
      model: '',
      unit: 'pcs',
      unitPrice: '',
      oemVendorId: '',
      leadTimeDays: '',
      warrantyMonths: '',
      description: '',
      imageUrl: '',
      datasheet: ''
    });
    setEditingProduct(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Product Catalog</h1>
          <p className="mt-2 text-gray-600">Manage your product inventory</p>
        </div>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          + Add Product
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Categories</option>
          <option value="hardware">Hardware</option>
          <option value="software">Software</option>
          <option value="service">Service</option>
          <option value="material">Material</option>
          <option value="equipment">Equipment</option>
        </select>
      </div>

      {/* Products Table */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Brand/Model</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unit Price</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Warranty</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr><td colSpan="7" className="text-center py-8">Loading...</td></tr>
            ) : products.length === 0 ? (
              <tr><td colSpan="7" className="text-center py-8">No products found</td></tr>
            ) : (
              products.map((product) => (
                <tr key={product.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">{product.productCode}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{product.productName}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{product.brand} {product.model}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className="px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                      {product.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {product.unitPrice ? `₹${product.unitPrice.toLocaleString()}/${product.unit}` : '-'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {product.warrantyMonths ? `${product.warrantyMonths} months` : '-'}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <button
                      onClick={() => handleEdit(product)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(product.id)}
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
              <h2 className="text-2xl font-bold mb-4">{editingProduct ? 'Edit Product' : 'Add New Product'}</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Product Code *</label>
                    <input
                      type="text"
                      required
                      value={formData.productCode}
                      onChange={(e) => setFormData({...formData, productCode: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                      disabled={!!editingProduct}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Category *</label>
                    <select
                      required
                      value={formData.category}
                      onChange={(e) => setFormData({...formData, category: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="hardware">Hardware</option>
                      <option value="software">Software</option>
                      <option value="service">Service</option>
                      <option value="material">Material</option>
                      <option value="equipment">Equipment</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Product Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.productName}
                    onChange={(e) => setFormData({...formData, productName: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Brand *</label>
                    <input
                      type="text"
                      required
                      value={formData.brand}
                      onChange={(e) => setFormData({...formData, brand: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Model</label>
                    <input
                      type="text"
                      value={formData.model}
                      onChange={(e) => setFormData({...formData, model: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Unit Price (₹)</label>
                    <input
                      type="number"
                      value={formData.unitPrice}
                      onChange={(e) => setFormData({...formData, unitPrice: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Unit *</label>
                    <input
                      type="text"
                      required
                      value={formData.unit}
                      onChange={(e) => setFormData({...formData, unit: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="pcs, kg, ltr, etc."
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Lead Time (Days)</label>
                    <input
                      type="number"
                      value={formData.leadTimeDays}
                      onChange={(e) => setFormData({...formData, leadTimeDays: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Warranty (Months)</label>
                    <input
                      type="number"
                      value={formData.warrantyMonths}
                      onChange={(e) => setFormData({...formData, warrantyMonths: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
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
                    <label className="block text-sm font-medium text-gray-700">Image URL</label>
                    <input
                      type="url"
                      value={formData.imageUrl}
                      onChange={(e) => setFormData({...formData, imageUrl: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Datasheet URL</label>
                    <input
                      type="url"
                      value={formData.datasheet}
                      onChange={(e) => setFormData({...formData, datasheet: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
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
                    {editingProduct ? 'Update' : 'Create'} Product
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

export default Products;

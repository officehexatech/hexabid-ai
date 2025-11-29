import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function SuperAdmin() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [tenants, setTenants] = useState([]);
  const [adminActions, setAdminActions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTenant, setSelectedTenant] = useState(null);

  useEffect(() => {
    if (activeTab === 'dashboard') {
      fetchDashboard();
    } else if (activeTab === 'tenants') {
      fetchTenants();
    } else if (activeTab === 'actions') {
      fetchActions();
    }
  }, [activeTab]);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/super-admin/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      if (error.response?.status === 403) {
        alert('Access Denied: Super Admin privileges required');
      }
    }
    setLoading(false);
  };

  const fetchTenants = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/super-admin/tenants`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTenants(response.data.tenants || []);
    } catch (error) {
      console.error('Error fetching tenants:', error);
    }
    setLoading(false);
  };

  const fetchActions = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/super-admin/actions`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAdminActions(response.data.actions || []);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
    setLoading(false);
  };

  const updateTenantStatus = async (tenantId, newStatus) => {
    const reason = prompt('Enter reason for status change:');
    if (!reason) return;

    try {
      const token = localStorage.getItem('token');
      await axios.patch(`${API_URL}/api/super-admin/tenants/${tenantId}/status`, {
        status: newStatus,
        reason
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Tenant status updated successfully');
      fetchTenants();
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Failed to update tenant status');
    }
  };

  const updateTenantPlan = async (tenantId, newPlan) => {
    const reason = prompt('Enter reason for plan change:');
    if (!reason) return;

    try {
      const token = localStorage.getItem('token');
      await axios.patch(`${API_URL}/api/super-admin/tenants/${tenantId}/plan`, {
        plan: newPlan,
        reason
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Tenant plan updated successfully');
      fetchTenants();
    } catch (error) {
      console.error('Error updating plan:', error);
      alert('Failed to update tenant plan');
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">🔐 Super Admin Panel</h1>
        <p className="text-gray-600 mt-2">Manage all tenants and system settings</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
        <nav className="flex border-b">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-6 py-3 font-medium ${activeTab === 'dashboard' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
          >
            📊 Dashboard
          </button>
          <button
            onClick={() => setActiveTab('tenants')}
            className={`px-6 py-3 font-medium ${activeTab === 'tenants' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
          >
            🏢 Tenants
          </button>
          <button
            onClick={() => setActiveTab('actions')}
            className={`px-6 py-3 font-medium ${activeTab === 'actions' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
          >
            📝 Action Log
          </button>
        </nav>
      </div>

      {loading && (
        <div className="text-center py-8 text-gray-500">Loading...</div>
      )}

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && dashboardData && (
        <div>
          {/* Tenant Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-600 text-sm">Total Tenants</p>
              <p className="text-3xl font-bold text-blue-600">{dashboardData.tenants.total}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-600 text-sm">Active Tenants</p>
              <p className="text-3xl font-bold text-green-600">{dashboardData.tenants.active}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-600 text-sm">Trial Tenants</p>
              <p className="text-3xl font-bold text-yellow-600">{dashboardData.tenants.trial}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-600 text-sm">Suspended</p>
              <p className="text-3xl font-bold text-red-600">{dashboardData.tenants.suspended}</p>
            </div>
          </div>

          {/* Plans Distribution */}
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Plans Distribution</h2>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-2xl font-bold text-gray-700">{dashboardData.plans.free}</p>
                <p className="text-sm text-gray-600">Free</p>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <p className="text-2xl font-bold text-blue-600">{dashboardData.plans.startup}</p>
                <p className="text-sm text-gray-600">Startup</p>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <p className="text-2xl font-bold text-purple-600">{dashboardData.plans.professional}</p>
                <p className="text-sm text-gray-600">Professional</p>
              </div>
              <div className="text-center p-4 bg-indigo-50 rounded-lg">
                <p className="text-2xl font-bold text-indigo-600">{dashboardData.plans.enterprise}</p>
                <p className="text-sm text-gray-600">Enterprise</p>
              </div>
            </div>
          </div>

          {/* Revenue & Growth */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-3">💰 Revenue</h3>
              <p className="text-3xl font-bold text-green-600">₹{dashboardData.revenue.mrr.toLocaleString()}</p>
              <p className="text-sm text-gray-600 mt-1">Monthly Recurring Revenue</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-3">📈 Growth</h3>
              <p className="text-3xl font-bold text-blue-600">{dashboardData.growth.recent_signups_30d}</p>
              <p className="text-sm text-gray-600 mt-1">New Signups (30 days)</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-3">👥 Users</h3>
              <p className="text-3xl font-bold text-purple-600">{dashboardData.users.total}</p>
              <p className="text-sm text-gray-600 mt-1">Total Active Users</p>
            </div>
          </div>

          {/* Usage Stats */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">AI Usage Stats ({dashboardData.usage.current_month})</h2>
            <div className="grid grid-cols-3 gap-6">
              <div>
                <p className="text-gray-600 text-sm">AI Credits Used</p>
                <p className="text-2xl font-bold text-blue-600">{dashboardData.usage.total_ai_credits_used.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Tokens Consumed</p>
                <p className="text-2xl font-bold text-purple-600">{dashboardData.usage.total_tokens_consumed.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Total Cost</p>
                <p className="text-2xl font-bold text-green-600">₹{dashboardData.usage.total_cost_incurred.toFixed(2)}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tenants Tab */}
      {activeTab === 'tenants' && (
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h2 className="text-xl font-semibold">All Tenants ({tenants.length})</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tenant</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Members</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {tenants.map((tenant) => (
                  <tr key={tenant.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-medium text-gray-900">{tenant.name}</p>
                        <p className="text-sm text-gray-500">{tenant.id}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <select
                        value={tenant.plan}
                        onChange={(e) => updateTenantPlan(tenant.id, e.target.value)}
                        className="px-2 py-1 border rounded text-sm"
                      >
                        <option value="free">Free</option>
                        <option value="startup">Startup</option>
                        <option value="professional">Professional</option>
                        <option value="enterprise">Enterprise</option>
                      </select>
                    </td>
                    <td className="px-6 py-4">
                      <select
                        value={tenant.status}
                        onChange={(e) => updateTenantStatus(tenant.id, e.target.value)}
                        className={`px-2 py-1 border rounded text-sm ${
                          tenant.status === 'active' ? 'bg-green-50 text-green-700' :
                          tenant.status === 'trial' ? 'bg-yellow-50 text-yellow-700' :
                          'bg-red-50 text-red-700'
                        }`}
                      >
                        <option value="active">Active</option>
                        <option value="trial">Trial</option>
                        <option value="suspended">Suspended</option>
                        <option value="cancelled">Cancelled</option>
                      </select>
                    </td>
                    <td className="px-6 py-4 text-sm">{tenant.member_count || 0}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {new Date(tenant.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => setSelectedTenant(tenant)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Action Log Tab */}
      {activeTab === 'actions' && (
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h2 className="text-xl font-semibold">Admin Action Log</h2>
          </div>
          <div className="divide-y">
            {adminActions.map((action, index) => (
              <div key={index} className="p-4 hover:bg-gray-50">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{action.action_type}</p>
                    <p className="text-sm text-gray-600 mt-1">
                      Tenant: {action.target_tenant_id}
                    </p>
                    {action.details && (
                      <p className="text-sm text-gray-500 mt-1">
                        {JSON.stringify(action.details)}
                      </p>
                    )}
                  </div>
                  <p className="text-xs text-gray-500">
                    {new Date(action.performed_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tenant Details Modal */}
      {selectedTenant && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold">{selectedTenant.name}</h2>
              <button
                onClick={() => setSelectedTenant(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Tenant ID</p>
                  <p className="font-medium">{selectedTenant.id}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Plan</p>
                  <p className="font-medium capitalize">{selectedTenant.plan}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Status</p>
                  <p className="font-medium capitalize">{selectedTenant.status}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Members</p>
                  <p className="font-medium">{selectedTenant.member_count || 0}</p>
                </div>
              </div>
              {selectedTenant.current_usage && (
                <div className="border-t pt-4">
                  <h3 className="font-semibold mb-2">Current Month Usage</h3>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">AI Credits</p>
                      <p className="font-medium">{selectedTenant.current_usage.ai_credits_used}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Tokens</p>
                      <p className="font-medium">{selectedTenant.current_usage.ai_tokens_consumed}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Cost</p>
                      <p className="font-medium">₹{selectedTenant.current_usage.cost_incurred}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SuperAdmin;

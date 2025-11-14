import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const AIAgents = () => {
  const navigate = useNavigate();
  const [creditBalance, setCreditBalance] = useState(0);
  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pricing, setPricing] = useState(null);
  const [showWorkflowModal, setShowWorkflowModal] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  
  const [formData, setFormData] = useState({
    search_query: '',
    category: '',
    location: '',
    tender_number: '',
    document_text: '',
    pricing_strategy: 'competitive',
    target_margin: 12
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const [balanceRes, executionsRes, pricingRes] = await Promise.all([
        axios.get(`${API_URL}/credits/balance`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/ai-agents/executions`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/ai-agents/pricing`)
      ]);
      
      setCreditBalance(balanceRes.data.balance);
      setExecutions(executionsRes.data.executions);
      setPricing(pricingRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const workflows = [
    {
      id: 'discover_and_bid',
      name: 'Discover & Bid',
      description: 'AI discovers relevant tenders, parses documents, generates BOQ, and assembles complete bid',
      icon: '🚀',
      cost: pricing?.usage_costs.discover_and_bid || 55,
      agents: ['Tender Discovery', 'Document Parser', 'BOQ Generator', 'Document Assembly']
    },
    {
      id: 'parse_and_bid',
      name: 'Parse & Bid',
      description: 'Start from document parsing for known tender, generate BOQ, and assemble bid documents',
      icon: '📄',
      cost: pricing?.usage_costs.parse_and_bid || 45,
      agents: ['Document Parser', 'BOQ Generator', 'Document Assembly']
    },
    {
      id: 'generate_boq',
      name: 'Generate BOQ',
      description: 'AI generates detailed Bill of Quantities with competitive pricing',
      icon: '💰',
      cost: pricing?.usage_costs.boq_generator || 20,
      agents: ['BOQ Generator']
    },
    {
      id: 'assemble_documents',
      name: 'Assemble Documents',
      description: 'AI assembles professional tender submission documents',
      icon: '📋',
      cost: pricing?.usage_costs.document_assembly || 10,
      agents: ['Document Assembly']
    }
  ];

  const handleExecuteWorkflow = async () => {
    if (!selectedWorkflow) return;
    
    // Check if user has enough credits
    const cost = workflows.find(w => w.id === selectedWorkflow).cost;
    if (creditBalance < cost) {
      alert(`Insufficient credits. You need ${cost} credits but have ${creditBalance}. Please purchase more credits.`);
      navigate('/credits');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      
      // Prepare input based on workflow type
      let input_data = {};
      
      if (selectedWorkflow === 'discover_and_bid') {
        input_data = {
          search_query: formData.search_query,
          category: formData.category,
          location: formData.location,
          pricing_strategy: formData.pricing_strategy,
          target_margin: parseInt(formData.target_margin)
        };
      } else if (selectedWorkflow === 'parse_and_bid') {
        input_data = {
          tender_number: formData.tender_number,
          document_text: formData.document_text,
          pricing_strategy: formData.pricing_strategy,
          target_margin: parseInt(formData.target_margin)
        };
      } else if (selectedWorkflow === 'generate_boq') {
        input_data = {
          tender_id: formData.tender_number,
          boq_items: [],
          pricing_strategy: formData.pricing_strategy,
          target_margin: parseInt(formData.target_margin)
        };
      } else if (selectedWorkflow === 'assemble_documents') {
        input_data = {
          tender_info: { tender_number: formData.tender_number }
        };
      }

      const response = await axios.post(
        `${API_URL}/ai-agents/execute`,
        {
          workflow_type: selectedWorkflow,
          input_data: input_data
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      alert(`Workflow started! Execution ID: ${response.data.execution_id}\nCredits deducted: ${response.data.credits_deducted}`);
      
      setShowWorkflowModal(false);
      fetchData();
    } catch (error) {
      if (error.response?.status === 402) {
        alert(error.response.data.detail);
        navigate('/credits');
      } else {
        alert('Failed to execute workflow: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  const openWorkflowModal = (workflowId) => {
    setSelectedWorkflow(workflowId);
    setShowWorkflowModal(true);
  };

  const getStatusBadge = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      running: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">HexaBid AI Agents</h1>
          <p className="mt-2 text-gray-600">Automate tender bidding with multi-agent AI system</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-600">Available Credits</div>
          <div className="text-3xl font-bold text-blue-600">{creditBalance}</div>
          <button
            onClick={() => navigate('/credits')}
            className="mt-2 text-sm text-blue-600 hover:text-blue-800"
          >
            Purchase Credits →
          </button>
        </div>
      </div>

      {/* Workflow Cards */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Available Workflows</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {workflows.map((workflow) => (
            <div key={workflow.id} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-3xl">{workflow.icon}</span>
                    <h3 className="text-lg font-semibold">{workflow.name}</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{workflow.description}</p>
                  <div className="mb-3">
                    <div className="text-xs text-gray-500 mb-1">Agents involved:</div>
                    <div className="flex flex-wrap gap-1">
                      {workflow.agents.map((agent, i) => (
                        <span key={i} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                          {agent}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between pt-4 border-t">
                <div className="text-lg font-semibold text-green-600">
                  {workflow.cost} Credits
                </div>
                <button
                  onClick={() => openWorkflowModal(workflow.id)}
                  disabled={creditBalance < workflow.cost}
                  className={`px-4 py-2 rounded-lg font-medium transition ${
                    creditBalance < workflow.cost
                      ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {creditBalance < workflow.cost ? 'Insufficient Credits' : 'Execute'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Execution History */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Execution History</h2>
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Workflow</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Credits</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                <tr><td colSpan="5" className="text-center py-8">Loading...</td></tr>
              ) : executions.length === 0 ? (
                <tr><td colSpan="5" className="text-center py-8">No executions yet. Start by running a workflow above!</td></tr>
              ) : (
                executions.map((exec) => (
                  <tr key={exec.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium">{exec.workflow_type.replace(/_/g, ' ').toUpperCase()}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusBadge(exec.status)}`}>
                        {exec.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm">{exec.credits_used || 0}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(exec.createdAt).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <button
                        onClick={() => navigate(`/ai-agents/${exec.id}`)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Workflow Execution Modal */}
      {showWorkflowModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
            <h2 className="text-2xl font-bold mb-4">Execute: {workflows.find(w => w.id === selectedWorkflow)?.name}</h2>
            
            <div className="space-y-4">
              {selectedWorkflow === 'discover_and_bid' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Search Query *</label>
                    <input
                      type="text"
                      placeholder="e.g., IT infrastructure, laptops, networking equipment"
                      value={formData.search_query}
                      onChange={(e) => setFormData({...formData, search_query: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Category</label>
                      <input
                        type="text"
                        placeholder="e.g., IT Hardware"
                        value={formData.category}
                        onChange={(e) => setFormData({...formData, category: e.target.value})}
                        className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Location</label>
                      <input
                        type="text"
                        placeholder="e.g., Delhi, All India"
                        value={formData.location}
                        onChange={(e) => setFormData({...formData, location: e.target.value})}
                        className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                  </div>
                </>
              )}
              
              {(selectedWorkflow === 'parse_and_bid' || selectedWorkflow === 'generate_boq' || selectedWorkflow === 'assemble_documents') && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">Tender Number *</label>
                  <input
                    type="text"
                    placeholder="e.g., TND-2025-001"
                    value={formData.tender_number}
                    onChange={(e) => setFormData({...formData, tender_number: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              )}
              
              {selectedWorkflow === 'parse_and_bid' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">Document Text (Optional)</label>
                  <textarea
                    rows="4"
                    placeholder="Paste tender document text here (optional)"
                    value={formData.document_text}
                    onChange={(e) => setFormData({...formData, document_text: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              )}

              {(selectedWorkflow === 'discover_and_bid' || selectedWorkflow === 'parse_and_bid' || selectedWorkflow === 'generate_boq') && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Pricing Strategy</label>
                    <select
                      value={formData.pricing_strategy}
                      onChange={(e) => setFormData({...formData, pricing_strategy: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="competitive">Competitive (L1 Focus)</option>
                      <option value="premium">Premium Quality</option>
                      <option value="cost_plus">Cost Plus</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Target Margin (%)</label>
                    <input
                      type="number"
                      value={formData.target_margin}
                      onChange={(e) => setFormData({...formData, target_margin: e.target.value})}
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>
              )}

              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="flex justify-between items-center">
                  <span className="font-medium">Credits Required:</span>
                  <span className="text-xl font-bold text-blue-600">
                    {workflows.find(w => w.id === selectedWorkflow)?.cost}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => { setShowWorkflowModal(false); setSelectedWorkflow(null); }}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleExecuteWorkflow}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                Execute Workflow
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIAgents;

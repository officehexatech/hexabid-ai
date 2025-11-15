import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function AIWorkspace() {
  const { tenderId } = useParams();
  const navigate = useNavigate();
  const [tender, setTender] = useState(null);
  const [workflow, setWorkflow] = useState('full'); // full, parse_bid, pricing_only
  const [executing, setExecuting] = useState(false);
  const [executionId, setExecutionId] = useState(null);
  const [progress, setProgress] = useState([]);

  useEffect(() => {
    if (tenderId) {
      fetchTenderDetails();
    }
  }, [tenderId]);

  const fetchTenderDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/tenders/${tenderId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTender(response.data);
    } catch (error) {
      console.error('Error fetching tender:', error);
    }
  };

  const startAIWorkflow = async () => {
    setExecuting(true);
    setProgress([]);
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/api/ai-agents/execute`, {
        workflow_type: workflow,
        tender_id: tenderId,
        tender_data: tender
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setExecutionId(response.data.execution_id);
      
      // Simulate progress updates
      simulateProgress();
      
    } catch (error) {
      console.error('Error starting workflow:', error);
      alert('Failed to start AI workflow: ' + (error.response?.data?.detail || error.message));
      setExecuting(false);
    }
  };

  const simulateProgress = () => {
    const steps = [
      { agent: 'Tender Discovery', status: 'completed', time: 2000 },
      { agent: 'Document Parser', status: 'completed', time: 3000 },
      { agent: 'BOQ Generator', status: 'processing', time: 4000 },
      { agent: 'RFQ Vendor', status: 'pending', time: 5000 },
      { agent: 'Pricing Strategy', status: 'pending', time: 6000 },
      { agent: 'Risk Compliance', status: 'pending', time: 7000 },
      { agent: 'Document Assembly', status: 'pending', time: 8000 }
    ];

    steps.forEach((step, index) => {
      setTimeout(() => {
        setProgress(prev => [...prev, step]);
        if (index === steps.length - 1) {
          setExecuting(false);
        }
      }, step.time);
    });
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <button
          onClick={() => navigate('/ai-agents')}
          className="text-blue-600 hover:text-blue-800 mb-2"
        >
          ← Back to AI Agents
        </button>
        <h1 className="text-3xl font-bold text-gray-800">AI Workspace</h1>
        <p className="text-gray-600 mt-2">Process tender with AI agent workflow</p>
      </div>

      {/* Tender Info */}
      {tender && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Tender Details</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Tender Number</p>
              <p className="font-semibold">{tender.tender_number}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Title</p>
              <p className="font-semibold">{tender.title}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Organization</p>
              <p className="font-semibold">{tender.organization}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Value</p>
              <p className="font-semibold">₹{(tender.tender_value / 100000).toFixed(2)}L</p>
            </div>
          </div>
        </div>
      )}

      {/* Workflow Selection */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Select AI Workflow</h2>
        <div className="grid grid-cols-3 gap-4">
          <button
            onClick={() => setWorkflow('full')}
            className={`p-4 border-2 rounded-lg text-left transition ${
              workflow === 'full' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <h3 className="font-semibold mb-2">Full Workflow</h3>
            <p className="text-sm text-gray-600">Complete end-to-end tender processing with all 9 agents</p>
            <p className="text-xs text-blue-600 mt-2">~100 credits</p>
          </button>
          <button
            onClick={() => setWorkflow('parse_bid')}
            className={`p-4 border-2 rounded-lg text-left transition ${
              workflow === 'parse_bid' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <h3 className="font-semibold mb-2">Parse & Bid</h3>
            <p className="text-sm text-gray-600">Document parsing, BOQ generation, and bid preparation</p>
            <p className="text-xs text-blue-600 mt-2">~50 credits</p>
          </button>
          <button
            onClick={() => setWorkflow('pricing_only')}
            className={`p-4 border-2 rounded-lg text-left transition ${
              workflow === 'pricing_only' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <h3 className="font-semibold mb-2">Pricing Only</h3>
            <p className="text-sm text-gray-600">Pricing strategy and risk analysis only</p>
            <p className="text-xs text-blue-600 mt-2">~30 credits</p>
          </button>
        </div>
      </div>

      {/* Execution Controls */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <button
          onClick={startAIWorkflow}
          disabled={executing || !tender}
          className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
        >
          {executing ? '🤖 AI Processing...' : '🚀 Start AI Workflow'}
        </button>
      </div>

      {/* Progress Tracking */}
      {progress.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Workflow Progress</h2>
          <div className="space-y-3">
            {progress.map((step, index) => (
              <div key={index} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  step.status === 'completed' ? 'bg-green-500' :
                  step.status === 'processing' ? 'bg-blue-500 animate-pulse' :
                  'bg-gray-300'
                }`}>
                  {step.status === 'completed' ? '✓' : step.status === 'processing' ? '⟳' : '○'}
                </div>
                <div className="flex-1">
                  <p className="font-semibold">{step.agent}</p>
                  <p className="text-sm text-gray-600 capitalize">{step.status}</p>
                </div>
              </div>
            ))}
          </div>
          
          {!executing && (
            <button
              onClick={() => navigate(`/ai-agents/${executionId}`)}
              className="mt-4 w-full py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              View Complete Results
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default AIWorkspace;

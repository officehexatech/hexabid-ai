import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const AIExecutionDetails = () => {
  const { executionId } = useParams();
  const navigate = useNavigate();
  const [execution, setExecution] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('results');

  useEffect(() => {
    fetchExecution();
    // Poll for updates if status is pending or running
    const interval = setInterval(() => {
      if (execution?.status === 'pending' || execution?.status === 'running') {
        fetchExecution();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [executionId]);

  const fetchExecution = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/ai-agents/executions/${executionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setExecution(response.data);
    } catch (error) {
      console.error('Failed to fetch execution:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  if (!execution) {
    return <div className="text-center py-8">Execution not found</div>;
  }

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
          <button
            onClick={() => navigate('/ai-agents')}
            className="text-blue-600 hover:text-blue-800 mb-2 flex items-center gap-1"
          >
            ← Back to AI Agents
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Execution Details</h1>
          <p className="mt-2 text-gray-600">ID: {execution.execution_id}</p>
        </div>
        <div>
          <span className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusBadge(execution.status)}`}>
            {execution.status.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Overview */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <div className="text-sm text-gray-600">Workflow Type</div>
            <div className="text-lg font-semibold mt-1">{execution.workflow_type.replace(/_/g, ' ').toUpperCase()}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Credits Used</div>
            <div className="text-lg font-semibold mt-1 text-green-600">{execution.credits_used}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Created At</div>
            <div className="text-lg font-semibold mt-1">{new Date(execution.createdAt).toLocaleString()}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Completed At</div>
            <div className="text-lg font-semibold mt-1">
              {execution.completedAt ? new Date(execution.completedAt).toLocaleString() : 'In Progress...'}
            </div>
          </div>
        </div>
      </div>

      {/* Agents Timeline */}
      {execution.timeline && execution.timeline.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Agent Execution Timeline</h2>
          <div className="space-y-3">
            {execution.timeline.map((item, index) => (
              <div key={index} className="flex items-center gap-4">
                <div className={`w-3 h-3 rounded-full ${
                  item.status === 'success' ? 'bg-green-500' :
                  item.status === 'error' ? 'bg-red-500' :
                  'bg-blue-500'
                }`}></div>
                <div className="flex-1">
                  <div className="font-medium">{item.agent}</div>
                  <div className="text-sm text-gray-600">{item.timestamp}</div>
                </div>
                <div>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusBadge(item.status)}`}>
                    {item.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <div className="flex">
            <button
              onClick={() => setActiveTab('results')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'results'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Results
            </button>
            <button
              onClick={() => setActiveTab('input')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'input'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Input Data
            </button>
            <button
              onClick={() => setActiveTab('logs')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'logs'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Execution Logs
            </button>
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'results' && (
            <div>
              {execution.status === 'completed' && execution.results ? (
                <div className="space-y-4">
                  {Object.keys(execution.results).map((key) => (
                    <div key={key} className="border-b pb-4">
                      <h3 className="font-semibold text-lg mb-2 capitalize">{key}</h3>
                      <pre className="bg-gray-50 p-4 rounded overflow-x-auto text-sm">
                        {JSON.stringify(execution.results[key], null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : execution.status === 'failed' ? (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="font-semibold text-red-800">Execution Failed</div>
                  <div className="text-red-700 mt-2">{execution.error || 'Unknown error'}</div>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  {execution.status === 'pending' ? 'Execution pending...' : 'Execution in progress...'}
                </div>
              )}
            </div>
          )}

          {activeTab === 'input' && (
            <pre className="bg-gray-50 p-4 rounded overflow-x-auto text-sm">
              {JSON.stringify(execution.input_data, null, 2)}
            </pre>
          )}

          {activeTab === 'logs' && (
            <div>
              {execution.workflow_log && execution.workflow_log.length > 0 ? (
                <div className="space-y-2">
                  {execution.workflow_log.map((log, index) => (
                    <div key={index} className="bg-gray-50 p-3 rounded">
                      <div className="flex justify-between items-start mb-1">
                        <span className="font-medium">{log.stage}</span>
                        <span className="text-sm text-gray-600">{log.timestamp}</span>
                      </div>
                      <pre className="text-xs overflow-x-auto">{JSON.stringify(log.data, null, 2)}</pre>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">No logs available</div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIExecutionDetails;

import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Save, Trash2, Download, ArrowLeft, Calculator } from 'lucide-react';
import { toast } from 'sonner';
import Layout from '../components/Layout';
import api from '../lib/api';

export default function BOQPage() {
  const { tenderId } = useParams();
  const queryClient = useQueryClient();
  const [editingId, setEditingId] = useState<string | null>(null);

  const { data: boqData, isLoading } = useQuery({
    queryKey: ['boq', tenderId],
    queryFn: async () => {
      const response = await api.get(`/boq/tender/${tenderId}`);
      return response.data;
    },
  });

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: any) => {
      const response = await api.patch(`/boq/items/${id}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['boq', tenderId] });
      toast.success('BOQ item updated');
      setEditingId(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/boq/items/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['boq', tenderId] });
      toast.success('BOQ item deleted');
    },
  });

  const generateMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post(`/boq/tender/${tenderId}/generate`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['boq', tenderId] });
      toast.success('BOQ generated successfully');
    },
  });

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <Link
            to={`/tenders/${tenderId}`}
            className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Tender</span>
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Bill of Quantities</h1>
              <p className="text-gray-600 mt-1">Manage tender items, quantities, and pricing</p>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => generateMutation.mutate()}
                disabled={generateMutation.isPending}
                className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2.5 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                <Calculator className="w-5 h-5" />
                <span>Auto-Generate</span>
              </button>
              <button className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2.5 rounded-lg hover:bg-primary-700 transition-colors">
                <Plus className="w-5 h-5" />
                <span>Add Item</span>
              </button>
            </div>
          </div>
        </div>

        {/* Summary Cards */}
        {boqData?.summary && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-sm text-gray-600 mb-1">Total Items</p>
              <p className="text-2xl font-bold text-gray-900">{boqData.summary.totalItems}</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-sm text-gray-600 mb-1">Subtotal</p>
              <p className="text-2xl font-bold text-gray-900">
                ₹{(boqData.summary.subtotal / 100000).toFixed(2)}L
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-sm text-gray-600 mb-1">Total GST</p>
              <p className="text-2xl font-bold text-gray-900">
                ₹{(boqData.summary.totalGst / 100000).toFixed(2)}L
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-green-200 p-4 bg-green-50">
              <p className="text-sm text-green-600 mb-1">Grand Total</p>
              <p className="text-2xl font-bold text-green-900">
                ₹{(boqData.summary.grandTotal / 100000).toFixed(2)}L
              </p>
            </div>
          </div>
        )}

        {/* BOQ Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full" data-testid="boq-table">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Item #</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Description</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Qty</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Unit</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Rate</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Amount</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">GST %</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase">Total</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-600 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {isLoading ? (
                  <tr>
                    <td colSpan={9} className="px-4 py-8 text-center text-gray-500">
                      Loading BOQ items...
                    </td>
                  </tr>
                ) : boqData?.items?.length > 0 ? (
                  boqData.items.map((item: any) => (
                    <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-sm">{item.itemNumber || '-'}</td>
                      <td className="px-4 py-3">
                        <div>
                          <p className="text-sm font-medium text-gray-900">{item.description}</p>
                          {item.specifications && (
                            <p className="text-xs text-gray-500 mt-1">{item.specifications}</p>
                          )}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm font-medium">{item.quantity}</td>
                      <td className="px-4 py-3 text-sm">{item.unit}</td>
                      <td className="px-4 py-3 text-sm font-medium">₹{item.finalRate?.toLocaleString()}</td>
                      <td className="px-4 py-3 text-sm">
                        ₹{(item.quantity * (item.finalRate || 0)).toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-sm">{item.gstPercentage}%</td>
                      <td className="px-4 py-3 text-sm font-medium text-green-600">
                        ₹{((item.quantity * (item.finalRate || 0)) * (1 + item.gstPercentage / 100)).toLocaleString()}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-end space-x-2">
                          <button
                            onClick={() => setEditingId(item.id)}
                            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                            title="Edit"
                          >
                            <Save className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => deleteMutation.mutate(item.id)}
                            className="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={9} className="px-4 py-12 text-center">
                      <div className="text-gray-500">
                        <p className="text-lg font-medium mb-2">No BOQ items yet</p>
                        <p className="text-sm">Click "Auto-Generate" or "Add Item" to get started</p>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <Download className="w-4 h-4" />
              <span>Export Excel</span>
            </button>
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <Download className="w-4 h-4" />
              <span>Export PDF</span>
            </button>
          </div>
          <button className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium">
            Finalize BOQ
          </button>
        </div>
      </div>
    </Layout>
  );
}

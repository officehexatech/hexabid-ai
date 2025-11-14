import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Search, Filter, Star, Calendar, MapPin, Building2 } from 'lucide-react';
import Layout from '../components/Layout';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';

export default function TendersPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const { data: tenders, isLoading } = useQuery({
    queryKey: ['tenders', searchTerm, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (statusFilter !== 'all') params.append('status', statusFilter);
      const response = await api.get(`/tenders?${params}`);
      return response.data.data || [];
    },
  });

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Tenders</h1>
            <p className="text-gray-600 mt-1">Discover and manage tender opportunities</p>
          </div>
          <button
            className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2.5 rounded-lg hover:bg-primary-700 transition-colors shadow-sm"
            data-testid="create-tender-button"
          >
            <Plus className="w-5 h-5" />
            <span className="font-medium">Add Tender</span>
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div className="flex flex-col lg:flex-row lg:items-center space-y-4 lg:space-y-0 lg:space-x-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search tenders..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                data-testid="search-tenders-input"
              />
            </div>

            {/* Status Filter */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="discovered">Discovered</option>
              <option value="evaluated">Evaluated</option>
              <option value="workspace_created">Workspace Created</option>
              <option value="bid_in_progress">Bid in Progress</option>
              <option value="submitted">Submitted</option>
              <option value="won">Won</option>
              <option value="lost">Lost</option>
            </select>

            <button className="flex items-center space-x-2 px-4 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <Filter className="w-5 h-5" />
              <span>More Filters</span>
            </button>
          </div>
        </div>

        {/* Tenders List */}
        <div className="space-y-4">
          {isLoading ? (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-200 border-t-primary-600"></div>
              <p className="mt-4 text-gray-600">Loading tenders...</p>
            </div>
          ) : tenders && tenders.length > 0 ? (
            tenders.map((tender: any) => (
              <Link
                key={tender.id}
                to={`/tenders/${tender.id}`}
                className="block bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-primary-200 transition-all"
                data-testid="tender-card"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-start space-x-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors">
                            {tender.title}
                          </h3>
                          {tender.isStarred && (
                            <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                          )}
                        </div>
                        
                        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                          <span className="flex items-center">
                            <Building2 className="w-4 h-4 mr-1.5" />
                            {tender.buyerOrganization || 'N/A'}
                          </span>
                          <span className="flex items-center">
                            <MapPin className="w-4 h-4 mr-1.5" />
                            {tender.tenderLocation || tender.state || 'N/A'}
                          </span>
                          {tender.bidSubmissionEndDate && (
                            <span className="flex items-center">
                              <Calendar className="w-4 h-4 mr-1.5" />
                              Due: {new Date(tender.bidSubmissionEndDate).toLocaleDateString()}
                            </span>
                          )}
                        </div>

                        <div className="flex flex-wrap gap-2">
                          {tender.category && (
                            <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
                              {tender.category}
                            </span>
                          )}
                          {tender.tenderValue && (
                            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                              ₹{(tender.tenderValue / 100000).toFixed(2)}L
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="ml-4">
                    <span
                      className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                        tender.status === 'discovered'
                          ? 'bg-blue-100 text-blue-700'
                          : tender.status === 'submitted'
                          ? 'bg-purple-100 text-purple-700'
                          : tender.status === 'won'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {tender.status?.replace('_', ' ') || 'Unknown'}
                    </span>
                  </div>
                </div>
              </Link>
            ))
          ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
              <p className="text-gray-600">No tenders found. Try adjusting your filters.</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

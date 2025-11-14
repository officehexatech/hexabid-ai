import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Calendar, MapPin, Building2, FileText, Download } from 'lucide-react';
import Layout from '../components/Layout';

export default function TenderDetailPage() {
  const { id } = useParams();

  // Mock data - replace with API call
  const tender = {
    id,
    title: 'Supply of Laptops for Government Schools',
    tenderNumber: 'GEM/2024/B/1234567',
    buyerOrganization: 'Ministry of Education',
    category: 'IT Hardware',
    tenderValue: 5000000,
    bidSubmissionEndDate: '2024-03-15T17:00:00Z',
    tenderLocation: 'Delhi',
    status: 'discovered',
    description: 'Supply of 500 laptops with 3 years warranty for government schools across Delhi',
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Back Button */}
        <Link
          to="/tenders"
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Tenders</span>
        </Link>

        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{tender.title}</h1>
              <p className="text-gray-600">{tender.tenderNumber}</p>
            </div>
            <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg text-sm font-medium">
              {tender.status}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <div className="flex items-center space-x-3">
              <Building2 className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Organization</p>
                <p className="font-medium text-gray-900">{tender.buyerOrganization}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Calendar className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Deadline</p>
                <p className="font-medium text-gray-900">
                  {new Date(tender.bidSubmissionEndDate).toLocaleDateString()}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <MapPin className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Location</p>
                <p className="font-medium text-gray-900">{tender.tenderLocation}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Link
            to={`/boq/${id}`}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow text-center"
          >
            <FileText className="w-8 h-8 text-primary-600 mx-auto mb-2" />
            <p className="font-medium text-gray-900">View BOQ</p>
          </Link>
          <Link
            to={`/workspace/${id}`}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow text-center"
          >
            <FileText className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <p className="font-medium text-gray-900">Workspace</p>
          </Link>
          <button className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow text-center">
            <Download className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p className="font-medium text-gray-900">Documents</p>
          </button>
          <button className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow text-center">
            <FileText className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <p className="font-medium text-gray-900">Generate RFQ</p>
          </button>
        </div>

        {/* Details */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Tender Details</h2>
          <div className="prose max-w-none">
            <p className="text-gray-700">{tender.description}</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

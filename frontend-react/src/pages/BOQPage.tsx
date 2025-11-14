import React from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/Layout';

export default function BOQPage() {
  const { tenderId } = useParams();
  
  return (
    <Layout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Bill of Quantities</h1>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-gray-600">BOQ module coming soon for Tender ID: {tenderId}</p>
        </div>
      </div>
    </Layout>
  );
}

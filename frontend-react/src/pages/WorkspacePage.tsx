import React from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/Layout';

export default function WorkspacePage() {
  const { projectId } = useParams();
  
  return (
    <Layout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Project Workspace</h1>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-gray-600">Workspace module coming soon for Project: {projectId}</p>
        </div>
      </div>
    </Layout>
  );
}

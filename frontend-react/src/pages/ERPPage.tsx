import React from 'react';
import Layout from '../components/Layout';

export default function ERPPage() {
  return (
    <Layout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">ERP Suite</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Sales</h3>
            <p className="text-sm text-gray-600">Orders, Invoices, Payments</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Purchase</h3>
            <p className="text-sm text-gray-600">POs, Receipts, Vendor Management</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Inventory</h3>
            <p className="text-sm text-gray-600">Stock, Warehouses, Movements</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Projects</h3>
            <p className="text-sm text-gray-600">Tasks, Milestones, Expenses</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Accounting</h3>
            <p className="text-sm text-gray-600">Ledger, Journal, Reports</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">HRMS</h3>
            <p className="text-sm text-gray-600">Employees, Attendance, Payroll</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

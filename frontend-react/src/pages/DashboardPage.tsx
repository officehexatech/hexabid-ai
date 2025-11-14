import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Package, Users, Send, TrendingUp, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import Layout from '../components/Layout';

export default function DashboardPage() {
  const stats = [
    {
      name: 'Active Tenders',
      value: '24',
      change: '+12%',
      icon: FileText,
      color: 'bg-blue-500',
    },
    {
      name: 'Products',
      value: '1,247',
      change: '+5%',
      icon: Package,
      color: 'bg-green-500',
    },
    {
      name: 'Vendors',
      value: '89',
      change: '+8%',
      icon: Users,
      color: 'bg-purple-500',
    },
    {
      name: 'RFQ Sent',
      value: '156',
      change: '+23%',
      icon: Send,
      color: 'bg-orange-500',
    },
  ];

  const recentTenders = [
    {
      id: '1',
      title: 'Supply of Laptops for Government Schools',
      organization: 'Ministry of Education',
      value: '₹50,00,000',
      deadline: '2024-03-15',
      status: 'In Progress',
      statusColor: 'text-blue-700 bg-blue-100',
    },
    {
      id: '2',
      title: 'Office Furniture Procurement',
      organization: 'Delhi Municipal Corporation',
      value: '₹15,00,000',
      deadline: '2024-03-20',
      status: 'Pending Review',
      statusColor: 'text-yellow-700 bg-yellow-100',
    },
    {
      id: '3',
      title: 'Medical Equipment Supply',
      organization: 'State Health Department',
      value: '₹1,20,00,000',
      deadline: '2024-04-01',
      status: 'New',
      statusColor: 'text-green-700 bg-green-100',
    },
  ];

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's what's happening today.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => (
            <div key={stat.name} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                  <p className="text-sm text-green-600 mt-2 font-medium">{stat.change} from last month</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Recent Tenders */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Recent Tenders</h2>
            <Link
              to="/tenders"
              className="text-sm font-medium text-primary-600 hover:text-primary-700"
            >
              View all
            </Link>
          </div>
          <div className="divide-y divide-gray-200">
            {recentTenders.map((tender) => (
              <Link
                key={tender.id}
                to={`/tenders/${tender.id}`}
                className="block px-6 py-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-gray-900 mb-1">{tender.title}</h3>
                    <p className="text-sm text-gray-600">{tender.organization}</p>
                    <div className="flex items-center space-x-4 mt-2">
                      <span className="text-sm font-medium text-gray-900">{tender.value}</span>
                      <span className="text-sm text-gray-500 flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        Due: {new Date(tender.deadline).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${tender.statusColor}`}
                  >
                    {tender.status}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            to="/tenders?status=new"
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 p-3 rounded-lg group-hover:bg-green-200 transition-colors">
                <AlertCircle className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">8</p>
                <p className="text-sm text-gray-600">New Tenders</p>
              </div>
            </div>
          </Link>

          <Link
            to="/tenders?status=in_progress"
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-blue-100 p-3 rounded-lg group-hover:bg-blue-200 transition-colors">
                <Clock className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">12</p>
                <p className="text-sm text-gray-600">In Progress</p>
              </div>
            </div>
          </Link>

          <Link
            to="/tenders?status=submitted"
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-purple-100 p-3 rounded-lg group-hover:bg-purple-200 transition-colors">
                <CheckCircle className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">4</p>
                <p className="text-sm text-gray-600">Submitted</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </Layout>
  );
}

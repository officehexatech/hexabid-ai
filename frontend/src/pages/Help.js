import React from 'react';
import { Link } from 'react-router-dom';

const Help = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-3">
              <img src="https://customer-assets.emergentagent.com/job_tender-master-4/artifacts/9595dbly_1%20HexaBid%20Logo%20Sm.jpg" alt="HexaBid" className="h-10 w-auto" />
              <span className="text-2xl font-bold text-gray-900">HexaBid</span>
            </Link>
            <Link to="/" className="text-blue-600 hover:text-blue-700 font-semibold">← Back to Home</Link>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Help Center</h1>

        {/* Getting Started */}
        <section className="bg-white rounded-xl shadow-sm p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
          <div className="space-y-4 text-gray-600">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">1. Create Your Account</h3>
              <p>Click "Start Free" and register with your email. No credit card required. It's 100% free forever.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">2. Complete Your Company Profile</h3>
              <p>After registration, you'll be prompted to complete your company profile with basic information like company name, industry, tax ID, and authorized person details.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">3. Start Managing Tenders</h3>
              <p>Access your dashboard and start adding vendors, creating RFQs, and managing your tender pipeline.</p>
            </div>
          </div>
        </section>

        {/* Common Questions */}
        <section className="bg-white rounded-xl shadow-sm p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">How do I add vendors?</h3>
              <p className="text-gray-600">Go to the Vendors page and click "Add Vendor". Fill in the vendor details including company name, contact information, GSTIN, and other relevant details.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">How do I create an RFQ?</h3>
              <p className="text-gray-600">Navigate to the RFQ page, click "Create RFQ", enter RFQ details, add line items, select vendors, and submit. You can track responses from the same page.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Can I invite team members?</h3>
              <p className="text-gray-600">Yes! Go to Team Management and click "Invite Member". Enter their email and assign a role (Admin, Manager, or Viewer). They'll receive an invitation email.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">How does the AI chatbot work?</h3>
              <p className="text-gray-600">Click the blue AI button on the bottom right of any page. Ask questions about HexaBid features, tender management, or get guidance on using the platform.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Is my data secure?</h3>
              <p className="text-gray-600">Yes! We use bank-grade encryption, secure cloud infrastructure, and role-based access control. Your data is private and protected.</p>
            </div>
          </div>
        </section>

        {/* Contact Support */}
        <section className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">Need More Help?</h2>
          <p className="mb-6">Our support team is available 24/7 to assist you.</p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <h3 className="font-semibold mb-2">Call Us</h3>
              <p className="text-blue-100">+91 8806106575</p>
              <p className="text-blue-100">+91 9607500750</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <h3 className="font-semibold mb-2">Email Us</h3>
              <p className="text-blue-100">support@cctverp.com</p>
            </div>
          </div>
          <button
            onClick={() => window.open('https://wa.me/918806106575', '_blank')}
            className="mt-6 bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold transition"
          >
            WhatsApp Support
          </button>
        </section>
      </div>
    </div>
  );
};

export default Help;
import React from 'react';
import { Link } from 'react-router-dom';

const Privacy = () => {
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
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Privacy Policy</h1>
        <p className="text-gray-600 mb-8">Last updated: November 2024</p>

        <div className="bg-white rounded-xl shadow-sm p-8 space-y-8">
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Introduction</h2>
            <p className="text-gray-600 leading-relaxed">
              Snxwfairies Innovations Pvt. Ltd. ("HexaBid", "we", "us", or "our") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our HexaBid platform.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Information We Collect</h2>
            <div className="space-y-4 text-gray-600">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Personal Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Name, email address, phone number</li>
                  <li>Company information (name, industry, address, tax ID)</li>
                  <li>Login credentials (encrypted passwords)</li>
                  <li>Profile information</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Business Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Vendor details and contact information</li>
                  <li>RFQ data and quotations</li>
                  <li>Tender documents and BOQ information</li>
                  <li>Team member information</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Usage Information</h3>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Log data (IP address, browser type, device information)</li>
                  <li>Usage patterns and feature interactions</li>
                  <li>AI chatbot conversations</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">3. How We Use Your Information</h2>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>Provide, operate, and maintain the HexaBid platform</li>
              <li>Process tender management and RFQ operations</li>
              <li>Send notifications about tender deadlines and updates</li>
              <li>Improve and personalize user experience</li>
              <li>Analyze usage patterns to enhance features</li>
              <li>Provide customer support and respond to inquiries</li>
              <li>Detect and prevent fraud or security issues</li>
              <li>Comply with legal obligations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Data Security</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              We implement industry-standard security measures to protect your information:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>Encryption of data in transit and at rest</li>
              <li>Secure authentication with JWT tokens</li>
              <li>Role-based access control</li>
              <li>Regular security audits and updates</li>
              <li>Secure cloud infrastructure</li>
              <li>MongoDB with access controls</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Data Sharing and Disclosure</h2>
            <p className="text-gray-600 leading-relaxed mb-4">We do not sell your personal information. We may share information in the following circumstances:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li><strong>With Your Team:</strong> Information is shared with team members based on their assigned roles</li>
              <li><strong>Service Providers:</strong> Third-party services that help operate our platform (cloud hosting, AI services)</li>
              <li><strong>Legal Requirements:</strong> When required by law or to protect rights and safety</li>
              <li><strong>Business Transfers:</strong> In case of merger, acquisition, or asset sale</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Your Rights</h2>
            <p className="text-gray-600 leading-relaxed mb-4">You have the right to:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>Access your personal information</li>
              <li>Update or correct your information</li>
              <li>Delete your account and associated data</li>
              <li>Export your data</li>
              <li>Opt-out of marketing communications</li>
              <li>Withdraw consent for data processing</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Data Retention</h2>
            <p className="text-gray-600 leading-relaxed">
              We retain your information for as long as your account is active or as needed to provide services. You can request deletion of your account at any time. Some information may be retained for legal or legitimate business purposes.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Cookies and Tracking</h2>
            <p className="text-gray-600 leading-relaxed">
              We use cookies and similar technologies for authentication, preferences, and analytics. You can control cookie settings through your browser. Session cookies are used for maintaining logged-in state.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Third-Party Services</h2>
            <p className="text-gray-600 leading-relaxed mb-4">HexaBid integrates with:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>Google OAuth for authentication</li>
              <li>AI services for chatbot and document processing</li>
              <li>Cloud storage for file management</li>
              <li>WhatsApp for customer support</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Children's Privacy</h2>
            <p className="text-gray-600 leading-relaxed">
              HexaBid is not intended for users under 18 years of age. We do not knowingly collect information from children.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Changes to Privacy Policy</h2>
            <p className="text-gray-600 leading-relaxed">
              We may update this Privacy Policy periodically. We will notify users of significant changes via email or platform notifications. Continued use of the platform after changes constitutes acceptance.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Contact Us</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              If you have questions about this Privacy Policy or your data:
            </p>
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-gray-800"><strong>Snxwfairies Innovations Pvt. Ltd.</strong></p>
              <p className="text-gray-600">Email: support@hexabid.in</p>
              <p className="text-gray-600">Phone: +91 8806106575, +91 9607500750</p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Privacy;
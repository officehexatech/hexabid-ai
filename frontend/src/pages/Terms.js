import React from 'react';
import { Link } from 'react-router-dom';

const Terms = () => {
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
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Terms of Service</h1>
        <p className="text-gray-600 mb-8">Last updated: November 2024</p>

        <div className="bg-white rounded-xl shadow-sm p-8 space-y-8">
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-600 leading-relaxed">
              By accessing and using HexaBid ("the Platform"), provided by Snxwfairies Innovations Pvt. Ltd., you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use the Platform.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Service Description</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              HexaBid is an AI-powered tender management platform that provides:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>Tender discovery and tracking</li>
              <li>Bill of Quantities (BOQ) generation</li>
              <li>Vendor and RFQ management</li>
              <li>Document automation</li>
              <li>Team collaboration tools</li>
              <li>Analytics and reporting</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Free Service</h2>
            <p className="text-gray-600 leading-relaxed">
              HexaBid is provided free of charge with no subscription fees, trial periods, or credit card requirements. We reserve the right to introduce paid premium features in the future, which will be optional and clearly communicated to users.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">4. User Accounts</h2>
            <div className="space-y-4 text-gray-600">
              <p>You agree to:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>Provide accurate, current, and complete information during registration</li>
                <li>Maintain the security of your account credentials</li>
                <li>Notify us immediately of any unauthorized use</li>
                <li>Accept responsibility for all activities under your account</li>
                <li>Use the Platform only for lawful business purposes</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Acceptable Use</h2>
            <p className="text-gray-600 leading-relaxed mb-4">You agree NOT to:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>Use the Platform for any illegal or unauthorized purpose</li>
              <li>Attempt to gain unauthorized access to any part of the Platform</li>
              <li>Interfere with or disrupt the Platform's operation</li>
              <li>Upload malicious code, viruses, or harmful content</li>
              <li>Scrape, copy, or reverse engineer the Platform</li>
              <li>Use the Platform to transmit spam or unsolicited messages</li>
              <li>Impersonate others or misrepresent your affiliation</li>
              <li>Violate any applicable laws or regulations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Content and Intellectual Property</h2>
            <div className="space-y-4 text-gray-600">
              <h3 className="font-semibold text-gray-900">Your Content</h3>
              <p>You retain ownership of all data, documents, and content you upload. By using the Platform, you grant us a license to use, store, and process your content solely to provide the services.</p>
              
              <h3 className="font-semibold text-gray-900 mt-4">Our Content</h3>
              <p>All Platform software, design, features, and branding are owned by Snxwfairies Innovations Pvt. Ltd. You may not copy, modify, or distribute our proprietary content without permission.</p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">7. AI Features and Accuracy</h2>
            <p className="text-gray-600 leading-relaxed">
              HexaBid uses AI for document parsing, BOQ generation, and assistance. While we strive for accuracy, AI-generated content should be reviewed and verified by users. We are not liable for decisions made based solely on AI outputs. Users are responsible for final tender submissions and business decisions.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Data Backup and Loss</h2>
            <p className="text-gray-600 leading-relaxed">
              We implement regular backups and security measures. However, we recommend users maintain their own copies of critical documents. We are not liable for data loss due to system failures, user error, or force majeure events.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Third-Party Services</h2>
            <p className="text-gray-600 leading-relaxed">
              The Platform may integrate with third-party services (Google OAuth, WhatsApp, etc.). Your use of these services is subject to their respective terms and policies. We are not responsible for third-party service availability or performance.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Service Availability</h2>
            <p className="text-gray-600 leading-relaxed">
              We strive for 24/7 availability but do not guarantee uninterrupted service. We may perform maintenance, updates, or modifications that temporarily affect availability. We will provide advance notice when possible.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Limitation of Liability</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              To the fullest extent permitted by law:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-600">
              <li>The Platform is provided "as is" without warranties of any kind</li>
              <li>We are not liable for indirect, incidental, or consequential damages</li>
              <li>Our total liability shall not exceed the amount paid by you (if any) in the past 12 months</li>
              <li>We are not responsible for tender outcomes, awards, or business decisions</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Indemnification</h2>
            <p className="text-gray-600 leading-relaxed">
              You agree to indemnify and hold harmless Snxwfairies Innovations Pvt. Ltd., its affiliates, and employees from any claims, damages, or expenses arising from your use of the Platform, violation of these Terms, or infringement of third-party rights.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">13. Account Termination</h2>
            <div className="space-y-4 text-gray-600">
              <p>We may suspend or terminate your account if you:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>Violate these Terms of Service</li>
                <li>Engage in fraudulent or abusive behavior</li>
                <li>Compromise Platform security</li>
              </ul>
              <p className="mt-4">You may delete your account at any time through the Platform settings. Upon termination, your data will be deleted per our Privacy Policy.</p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">14. Modifications to Terms</h2>
            <p className="text-gray-600 leading-relaxed">
              We reserve the right to modify these Terms at any time. Significant changes will be communicated via email or Platform notifications. Continued use after modifications constitutes acceptance of the new Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">15. Governing Law</h2>
            <p className="text-gray-600 leading-relaxed">
              These Terms shall be governed by the laws of India. Any disputes shall be subject to the exclusive jurisdiction of courts in [Your City], India.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">16. Contact Information</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              For questions about these Terms of Service:
            </p>
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-gray-800"><strong>Snxwfairies Innovations Pvt. Ltd.</strong></p>
              <p className="text-gray-600">Email: support@cctverp.com</p>
              <p className="text-gray-600">Phone: +91 8806106575, +91 9607500750</p>
            </div>
          </section>

          <section className="border-t pt-6">
            <p className="text-gray-600 leading-relaxed">
              By using HexaBid, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Terms;
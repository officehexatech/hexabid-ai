import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

const Credits = () => {
  const [balance, setBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingPayment, setProcessingPayment] = useState(false);

  useEffect(() => {
    fetchData();
    loadRazorpayScript();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const [balanceRes, transactionsRes, packagesRes] = await Promise.all([
        axios.get(`${API_URL}/credits/balance`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/credits/transactions`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/payments/packages`)
      ]);
      
      setBalance(balanceRes.data);
      setTransactions(transactionsRes.data.transactions);
      setPackages(packagesRes.data.packages);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRazorpayScript = () => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);
  };

  const handlePurchase = async (pkg) => {
    try {
      setProcessingPayment(true);
      const token = localStorage.getItem('token');
      
      // Create order
      const orderRes = await axios.post(
        `${API_URL}/payments/create-order`,
        {
          amount: pkg.price * 100, // Convert to paise
          credits: pkg.credits + pkg.bonus,
          currency: 'INR'
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const options = {
        key: orderRes.data.key_id,
        amount: orderRes.data.amount,
        currency: orderRes.data.currency,
        order_id: orderRes.data.order_id,
        name: 'HexaBid',
        description: `Purchase ${pkg.credits + pkg.bonus} AI Credits`,
        image: '/logo.png',
        handler: async function (response) {
          try {
            // Verify payment
            await axios.post(
              `${API_URL}/payments/verify`,
              {
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature
              },
              { headers: { Authorization: `Bearer ${token}` } }
            );
            
            alert('Payment successful! Credits added to your account.');
            fetchData();
          } catch (error) {
            alert('Payment verification failed: ' + error.message);
          } finally {
            setProcessingPayment(false);
          }
        },
        prefill: {
          name: '',
          email: '',
          contact: ''
        },
        theme: {
          color: '#2563eb'
        },
        modal: {
          ondismiss: function() {
            setProcessingPayment(false);
          }
        }
      };

      const razorpay = new window.Razorpay(options);
      razorpay.open();
    } catch (error) {
      console.error('Payment error:', error);
      alert('Failed to initiate payment: ' + error.message);
      setProcessingPayment(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Credits</h1>
        <p className="mt-2 text-gray-600">Purchase credits to use HexaBid AI Agents</p>
      </div>

      {/* Current Balance */}
      <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg p-8 text-white">
        <div className="flex justify-between items-center">
          <div>
            <div className="text-blue-100 text-sm">Available Balance</div>
            <div className="text-5xl font-bold mt-2">{balance?.balance || 0}</div>
            <div className="text-blue-100 text-sm mt-2">Credits</div>
          </div>
          <div className="text-right">
            <div className="text-sm text-blue-100">Total Purchased</div>
            <div className="text-2xl font-semibold">{balance?.total_purchased || 0}</div>
            <div className="text-sm text-blue-100 mt-3">Total Used</div>
            <div className="text-2xl font-semibold">{balance?.total_used || 0}</div>
          </div>
        </div>
      </div>

      {/* Credit Packages */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Purchase Credits</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {packages.map((pkg, index) => (
            <div
              key={index}
              className={`bg-white border-2 rounded-lg p-6 hover:shadow-lg transition ${
                pkg.bonus > 0 ? 'border-green-500' : 'border-gray-200'
              }`}
            >
              {pkg.bonus > 0 && (
                <div className="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full inline-block mb-3">
                  {Math.round((pkg.bonus / pkg.credits) * 100)}% BONUS
                </div>
              )}
              
              <div className="text-center">
                <div className="text-4xl font-bold text-gray-900">{pkg.credits}</div>
                {pkg.bonus > 0 && (
                  <div className="text-sm text-green-600 font-medium">+ {pkg.bonus} Bonus</div>
                )}
                <div className="text-sm text-gray-600 mt-1">Credits</div>
                
                <div className="mt-4 mb-4">
                  <div className="text-3xl font-bold text-blue-600">₹{pkg.price}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    ₹{(pkg.price / (pkg.credits + pkg.bonus)).toFixed(2)} per credit
                  </div>
                </div>

                <button
                  onClick={() => handlePurchase(pkg)}
                  disabled={processingPayment}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {processingPayment ? 'Processing...' : 'Buy Now'}
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-start gap-2">
            <svg className="h-5 w-5 text-blue-600 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="text-sm text-blue-900">
              <strong>Payment Methods:</strong> UPI, Cards, Net Banking, Wallets. Powered by Razorpay. All transactions are secure and encrypted.
            </div>
          </div>
        </div>
      </div>

      {/* Transaction History */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Transaction History</h2>
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance After</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transactions.length === 0 ? (
                <tr><td colSpan="5" className="text-center py-8 text-gray-500">No transactions yet</td></tr>
              ) : (
                transactions.map((txn) => (
                  <tr key={txn.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(txn.createdAt).toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        txn.type === 'purchase' ? 'bg-green-100 text-green-800' :
                        txn.type === 'usage' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {txn.type}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{txn.description}</td>
                    <td className="px-6 py-4 text-sm font-medium">
                      <span className={txn.amount > 0 ? 'text-green-600' : 'text-red-600'}>
                        {txn.amount > 0 ? '+' : ''}{txn.amount}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{txn.balance_after}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Credits;

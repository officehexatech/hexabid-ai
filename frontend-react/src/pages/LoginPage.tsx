import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';
import { Mail, Lock } from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import api from '../lib/api';

export default function LoginPage() {
  const [step, setStep] = useState<'email' | 'otp'>('email');
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);
  const { register, handleSubmit, formState: { errors } } = useForm();

  const requestOtp = async (data: any) => {
    setIsLoading(true);
    try {
      await api.post('/auth/request-otp', { email: data.email });
      setEmail(data.email);
      setStep('otp');
      toast.success('OTP sent to your email');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to send OTP');
    } finally {
      setIsLoading(false);
    }
  };

  const verifyOtp = async (data: any) => {
    setIsLoading(true);
    try {
      const response = await api.post('/auth/verify-otp', {
        email,
        otp: data.otp,
      });
      const { user, accessToken, refreshToken } = response.data;
      setAuth(user, accessToken, refreshToken);
      toast.success('Login successful!');
      navigate('/');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Invalid OTP');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl mb-4 shadow-lg">
            <span className="text-white font-bold text-2xl">H</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to HexaBid</h1>
          <p className="text-gray-600">Multi-tenant Tender & ERP Platform</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          {step === 'email' ? (
            <form onSubmit={handleSubmit(requestOtp)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    {...register('email', {
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address',
                      },
                    })}
                    type="email"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
                    placeholder="your@email.com"
                    data-testid="email-input"
                  />
                </div>
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600">{errors.email.message as string}</p>
                )}
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-primary-500 to-primary-600 text-white py-3 rounded-lg font-medium hover:from-primary-600 hover:to-primary-700 focus:ring-4 focus:ring-primary-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="request-otp-button"
              >
                {isLoading ? 'Sending...' : 'Send OTP'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleSubmit(verifyOtp)} className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Enter OTP
                  </label>
                  <button
                    type="button"
                    onClick={() => setStep('email')}
                    className="text-sm text-primary-600 hover:text-primary-700"
                  >
                    Change email
                  </button>
                </div>
                <p className="text-sm text-gray-600 mb-4">OTP sent to {email}</p>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    {...register('otp', {
                      required: 'OTP is required',
                      minLength: { value: 6, message: 'OTP must be 6 digits' },
                      maxLength: { value: 6, message: 'OTP must be 6 digits' },
                    })}
                    type="text"
                    maxLength={6}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors text-center text-2xl font-mono tracking-widest"
                    placeholder="000000"
                    data-testid="otp-input"
                  />
                </div>
                {errors.otp && (
                  <p className="mt-1 text-sm text-red-600">{errors.otp.message as string}</p>
                )}
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-primary-500 to-primary-600 text-white py-3 rounded-lg font-medium hover:from-primary-600 hover:to-primary-700 focus:ring-4 focus:ring-primary-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="verify-otp-button"
              >
                {isLoading ? 'Verifying...' : 'Verify & Login'}
              </button>
            </form>
          )}

          <p className="mt-6 text-center text-xs text-gray-500">
            By continuing, you agree to HexaBid's Terms of Service and Privacy Policy
          </p>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm font-medium text-blue-900 mb-2">Demo Access:</p>
          <p className="text-xs text-blue-700">Use any email to receive OTP in console logs (development mode)</p>
        </div>
      </div>
    </div>
  );
}

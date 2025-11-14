import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Vendors from './pages/Vendors';
import RFQ from './pages/RFQ';
import CompanyProfile from './pages/CompanyProfile';
import TeamManagement from './pages/TeamManagement';
import VerifyEmail from './pages/VerifyEmail';
import Layout from './components/Layout';
import './App.css';

const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
};

const ProfileCompletionCheck = ({ children }) => {
  const { user } = useAuth();
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  // Redirect to profile completion if not completed
  if (!user.hasCompletedProfile && window.location.pathname !== '/company-profile') {
    return <Navigate to="/company-profile" />;
  }
  
  return children;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          
          {/* Protected Routes */}
          <Route path="/company-profile" element={
            <PrivateRoute>
              <CompanyProfile />
            </PrivateRoute>
          } />
          
          <Route path="/" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/vendors" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <Vendors />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/rfq" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <RFQ />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/team" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <TeamManagement />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
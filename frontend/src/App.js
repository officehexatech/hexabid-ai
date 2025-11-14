import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Vendors from './pages/Vendors';
import RFQ from './pages/RFQ';
import CompanyProfile from './pages/CompanyProfile';
import TeamManagement from './pages/TeamManagement';
import VerifyEmail from './pages/VerifyEmail';
import Help from './pages/Help';
import Feedback from './pages/Feedback';
import Privacy from './pages/Privacy';
import Terms from './pages/Terms';
import AdminSettings from './pages/AdminSettings';
import Tenders from './pages/Tenders';
import Products from './pages/Products';
import BOQManagement from './pages/BOQManagement';
import Notifications from './pages/Notifications';
import AIAgents from './pages/AIAgents';
import Credits from './pages/Credits';
import AIExecutionDetails from './pages/AIExecutionDetails';
import GEMIntegration from './pages/GEMIntegration';
import CompetitorAnalysis from './pages/CompetitorAnalysis';
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
  
  if (!user.hasCompletedProfile && window.location.pathname !== '/company-profile') {
    return <Navigate to="/company-profile" />;
  }
  
  return children;
};

const PublicRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? <Navigate to="/dashboard" /> : children;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/help" element={<Help />} />
          <Route path="/feedback" element={<Feedback />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/terms" element={<Terms />} />
          
          <Route path="/login" element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } />
          
          <Route path="/register" element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          } />
          
          <Route path="/verify-email" element={<VerifyEmail />} />
          
          <Route path="/company-profile" element={
            <PrivateRoute>
              <CompanyProfile />
            </PrivateRoute>
          } />
          
          <Route path="/dashboard" element={
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
          
          <Route path="/admin/settings" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <AdminSettings />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/tenders" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <Tenders />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/products" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <Products />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/boq" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <BOQManagement />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/notifications" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <Notifications />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/ai-agents" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <AIAgents />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/ai-agents/:executionId" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <AIExecutionDetails />
                </Layout>
              </ProfileCompletionCheck>
            </PrivateRoute>
          } />
          
          <Route path="/credits" element={
            <PrivateRoute>
              <ProfileCompletionCheck>
                <Layout>
                  <Credits />
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
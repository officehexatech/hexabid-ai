import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import { useAuthStore } from './store/authStore';

// Pages
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import TendersPage from './pages/TendersPage';
import TenderDetailPage from './pages/TenderDetailPage';
import BOQPage from './pages/BOQPage';
import ProductsPage from './pages/ProductsPage';
import VendorsPage from './pages/VendorsPage';
import RFQPage from './pages/RFQPage';
import DocumentsPage from './pages/DocumentsPage';
import WorkspacePage from './pages/WorkspacePage';
import ERPPage from './pages/ERPPage';
import AnalyticsPage from './pages/AnalyticsPage';
import SettingsPage from './pages/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toaster position="top-right" richColors />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          <Route
            path="/"
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/tenders"
            element={
              <PrivateRoute>
                <TendersPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/tenders/:id"
            element={
              <PrivateRoute>
                <TenderDetailPage />
              </PrivateRoute>
            }
          />

          <Route
            path="/boq/:tenderId"
            element={
              <PrivateRoute>
                <BOQPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/products"
            element={
              <PrivateRoute>
                <ProductsPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/vendors"
            element={
              <PrivateRoute>
                <VendorsPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/rfq"
            element={
              <PrivateRoute>
                <RFQPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/documents"
            element={
              <PrivateRoute>
                <DocumentsPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/workspace/:projectId"
            element={
              <PrivateRoute>
                <WorkspacePage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/erp/*"
            element={
              <PrivateRoute>
                <ERPPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/analytics"
            element={
              <PrivateRoute>
                <AnalyticsPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/settings"
            element={
              <PrivateRoute>
                <SettingsPage />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;

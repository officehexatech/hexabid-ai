import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';
const EMERGENT_AUTH_URL = 'https://auth.emergentagent.com';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const interceptor = axios.interceptors.request.use(
      (config) => {
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    return () => axios.interceptors.request.eject(interceptor);
  }, [token]);

  useEffect(() => {
    const processGoogleAuth = async () => {
      // Check for session_id in URL fragment
      const hash = window.location.hash;
      if (hash && hash.includes('session_id=')) {
        const sessionId = hash.split('session_id=')[1].split('&')[0];
        
        try {
          // Process session with backend
          const response = await axios.post(
            `${API_URL}/auth/google/session`,
            {},
            { 
              headers: { 'X-Session-ID': sessionId },
              withCredentials: true 
            }
          );
          
          setUser(response.data.user);
          
          // Clean URL
          window.history.replaceState({}, document.title, window.location.pathname);
          setLoading(false);
          return;
        } catch (error) {
          console.error('Google auth failed:', error);
        }
      }
      
      // Load existing session
      loadUser();
    };

    processGoogleAuth();
  }, []);

  const loadUser = async () => {
    if (token) {
      try {
        const response = await axios.get(`${API_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true
        });
        setUser(response.data);
      } catch (error) {
        console.error('Failed to load user:', error);
        logout();
      }
    } else {
      // Try cookie-based auth
      try {
        const response = await axios.get(`${API_URL}/auth/me`, {
          withCredentials: true
        });
        setUser(response.data);
      } catch (error) {
        // No active session
      }
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    const response = await axios.post(`${API_URL}/auth/login`, { email, password });
    const { accessToken, user: userData } = response.data;
    setToken(accessToken);
    setUser(userData);
    localStorage.setItem('token', accessToken);
    return userData;
  };

  const register = async (email, password, fullName, phone) => {
    const response = await axios.post(`${API_URL}/auth/register`, {
      email,
      password,
      fullName,
      phone
    });
    const { accessToken, user: userData } = response.data;
    setToken(accessToken);
    setUser(userData);
    localStorage.setItem('token', accessToken);
    return userData;
  };

  const loginWithGoogle = () => {
    const redirectUrl = `${window.location.origin}/dashboard`;
    window.location.href = `${EMERGENT_AUTH_URL}/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const logout = async () => {
    try {
      await axios.post(`${API_URL}/auth/logout`, {}, { withCredentials: true });
    } catch (error) {
      console.error('Logout error:', error);
    }
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const refreshUser = async () => {
    if (token) {
      const response = await axios.get(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
        withCredentials: true
      });
      setUser(response.data);
    } else {
      const response = await axios.get(`${API_URL}/auth/me`, {
        withCredentials: true
      });
      setUser(response.data);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, loginWithGoogle, logout, loading, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
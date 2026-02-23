/**
 * API Service for PathFinder Admin Dashboard
 * Handles all HTTP requests to backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============= Auth API =============

export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// ============= Analytics API =============

export const analyticsAPI = {
  getDashboard: async () => {
    const response = await api.get('/analytics/dashboard');
    return response.data;
  },

  getUserTrend: async (days = 7) => {
    const response = await api.get(`/analytics/users/trend?days=${days}`);
    return response.data;
  },

  getSessionTrend: async (days = 7) => {
    const response = await api.get(`/analytics/sessions/trend?days=${days}`);
    return response.data;
  },

  getHazardDistribution: async () => {
    const response = await api.get('/analytics/hazards/distribution');
    return response.data;
  },
};

// ============= Complaints API =============

export const complaintsAPI = {
  getAll: async (status = null) => {
    const url = status ? `/complaints/?status_filter=${status}` : '/complaints/';
    const response = await api.get(url);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/complaints/${id}`);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.patch(`/complaints/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    await api.delete(`/complaints/${id}`);
  },
};

// ============= Sessions API =============

export const sessionsAPI = {
  getAll: async (limit = 100) => {
    const response = await api.get(`/sessions/?limit=${limit}`);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/sessions/${id}`);
    return response.data;
  },
};

export default api;

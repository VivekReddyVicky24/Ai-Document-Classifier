import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 30000;

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: parseInt(API_TIMEOUT),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: (credentials) => apiClient.post('/api/auth/login', credentials),
  register: (userData) => apiClient.post('/api/auth/register', userData),
  verifyToken: () => apiClient.get('/api/auth/verify'),
};

// Document API calls
export const documentAPI = {
  uploadFiles: (formData) =>
    apiClient.post('/api/uploads', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getHistory: (params) => apiClient.get('/api/uploads/history', { params }),
  getDocument: (id) => apiClient.get(`/api/uploads/${id}`),
  deleteDocument: (id) => apiClient.delete(`/api/uploads/${id}`),
};

export default apiClient;

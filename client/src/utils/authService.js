import { authAPI } from './api';

export const authService = {
  login: async (email, password) => {
    const response = await authAPI.login({ email, password });
    const { token, user } = response.data.data;
    if (token && user) {
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
    }
    return { token, user };
  },

  register: async (firstName, lastName, email, password) => {
    const response = await authAPI.register({
      name: `${firstName} ${lastName}`,
      email,
      password,
    });
    const { token, user } = response.data.data;
    if (token && user) {
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
    }
    return { token, user };
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getToken: () => localStorage.getItem('token'),

  getUser: () => {
    try {
      const user = localStorage.getItem('user');
      if (!user || user === 'undefined') {
        return null;
      }
      return JSON.parse(user);
    } catch (error) {
      console.error('Error parsing user from localStorage:', error);
      localStorage.removeItem('user');
      return null;
    }
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

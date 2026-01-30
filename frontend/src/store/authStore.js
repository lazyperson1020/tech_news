import { create } from 'zustand';
import { authAPI, profileAPI } from '../services/api';

const useAuthStore = create((set) => ({
  user: null,
  profile: null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,
  error: null,

  login: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const response = await authAPI.login(credentials);
      const { access, refresh } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      const profileResponse = await profileAPI.getMe();
      
      set({
        isAuthenticated: true,
        user: profileResponse.data.user,
        profile: profileResponse.data,
        loading: false,
      });
      
      return true;
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Login failed',
        loading: false,
      });
      return false;
    }
  },

  register: async (data) => {
    set({ loading: true, error: null });
    try {
      await authAPI.register(data);
      set({ loading: false });
      return true;
    } catch (error) {
      set({
        error: error.response?.data || 'Registration failed',
        loading: false,
      });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({
      user: null,
      profile: null,
      isAuthenticated: false,
    });
  },

  loadProfile: async () => {
    try {
      const response = await profileAPI.getMe();
      set({
        user: response.data.user,
        profile: response.data,
      });
    } catch (error) {
      console.error('Failed to load profile', error);
    }
  },

  updateProfile: async (data) => {
    try {
      const response = await profileAPI.updateMe(data);
      set({ profile: response.data });
      return true;
    } catch (error) {
      set({ error: 'Failed to update profile' });
      return false;
    }
  },
}));

export default useAuthStore;

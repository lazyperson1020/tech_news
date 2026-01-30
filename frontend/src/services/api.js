import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/token/refresh/`, {
          refresh,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/register/', data),
  login: (data) => api.post('/login/', data),
};

export const articlesAPI = {
  getAll: (params) => api.get('/articles/', { params }),
  getOne: (id) => api.get(`/articles/${id}/`),
  create: (data) => api.post('/articles/', data),
  update: (id, data) => api.patch(`/articles/${id}/`, data),
  delete: (id) => api.delete(`/articles/${id}/`),
  summarize: (id) => api.post(`/articles/${id}/summarize/`),
  fetchNews: (category) => api.post('/articles/fetch_news/', {}, { params: { category } }),
  trending: () => api.get('/articles/trending/'),
};

export const bookmarksAPI = {
  getAll: () => api.get('/bookmarks/'),
  create: (articleId) => api.post('/bookmarks/', { article_id: articleId }),
  remove: (articleId) => api.post('/bookmarks/remove/', { article_id: articleId }),
};

export const profileAPI = {
  getMe: () => api.get('/profiles/me/'),
  updateMe: (data) => api.patch('/profiles/me/', data),
};

export const preferencesAPI = {
  getMe: () => api.get('/preferences/me/'),
  updateMe: (data) => api.put('/preferences/me/', data),
};

export const analyticsAPI = {
  get: () => api.get('/analytics/'),
};

export default api;

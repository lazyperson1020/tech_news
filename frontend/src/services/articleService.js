import api from './api';

export const articleService = {
  getArticles: async (params = {}) => {
    const response = await api.get('/articles/articles/', { params });
    return response.data;
  },

  getArticle: async (slug) => {
    const response = await api.get(`/articles/articles/${slug}/`);
    return response.data;
  },

  createArticle: async (articleData) => {
    const response = await api.post('/articles/articles/', articleData);
    return response.data;
  },

  updateArticle: async (slug, articleData) => {
    const response = await api.put(`/articles/articles/${slug}/`, articleData);
    return response.data;
  },

  deleteArticle: async (slug) => {
    await api.delete(`/articles/articles/${slug}/`);
  },

  generateSummary: async (slug) => {
    const response = await api.post(`/articles/articles/${slug}/generate_summary/`);
    return response.data;
  },

  likeArticle: async (slug) => {
    const response = await api.post(`/articles/articles/${slug}/like/`);
    return response.data;
  },

  getTrending: async () => {
    const response = await api.get('/articles/articles/trending/');
    return response.data;
  },

  getFeatured: async () => {
    const response = await api.get('/articles/articles/featured/');
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/articles/categories/');
    return response.data;
  },

  // Bookmarks
  getBookmarks: async () => {
    const response = await api.get('/articles/bookmarks/');
    return response.data;
  },

  addBookmark: async (articleId) => {
    const response = await api.post('/articles/bookmarks/', { article_id: articleId });
    return response.data;
  },

  removeBookmark: async (bookmarkId) => {
    await api.delete(`/articles/bookmarks/${bookmarkId}/`);
  },

  // Comments
  getComments: async (articleId) => {
    const response = await api.get('/articles/comments/', { params: { article: articleId } });
    return response.data;
  },

  addComment: async (commentData) => {
    const response = await api.post('/articles/comments/', commentData);
    return response.data;
  },
};
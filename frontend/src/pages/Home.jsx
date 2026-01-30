import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { articlesAPI, bookmarksAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import '../styles/Home.css';

function Home() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');
  const [fetching, setFetching] = useState(false);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const navigate = useNavigate();

  const categories = [
    { value: '', label: 'All' },
    { value: 'ai_ml', label: 'AI/ML' },
    { value: 'blockchain', label: 'Blockchain' },
    { value: 'web_dev', label: 'Web Dev' },
    { value: 'app_dev', label: 'App Dev' },
    { value: 'cybersecurity', label: 'Cybersecurity' },
    { value: 'cloud', label: 'Cloud' },
  ];

  useEffect(() => {
    loadArticles();
  }, [category, search]);

  const loadArticles = async () => {
    setLoading(true);
    try {
      const params = {};
      if (category) params.category = category;
      if (search) params.search = search;
      
      const response = await articlesAPI.getAll(params);
      setArticles(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to load articles', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchNews = async () => {
    setFetching(true);
    try {
      await articlesAPI.fetchNews(category || 'general');
      await loadArticles();
      alert('News fetched successfully!');
    } catch (error) {
      alert('Failed to fetch news');
    } finally {
      setFetching(false);
    }
  };

  const handleBookmark = async (articleId, isBookmarked) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      if (isBookmarked) {
        await bookmarksAPI.remove(articleId);
      } else {
        await bookmarksAPI.create(articleId);
      }
      await loadArticles();
    } catch (error) {
      console.error('Bookmark action failed', error);
    }
  };

  return (
    <div className="home">
      <div className="controls">
        <div className="filters">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="filter-select"
          >
            {categories.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>

          <input
            type="text"
            placeholder="Search articles..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />

          {isAuthenticated && (
            <button onClick={handleFetchNews} disabled={fetching} className="fetch-btn">
              {fetching ? 'Fetching...' : 'Fetch Latest News'}
            </button>
          )}
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading articles...</div>
      ) : (
        <div className="articles-grid">
          {articles.length === 0 ? (
            <p className="no-articles">No articles found</p>
          ) : (
            articles.map((article) => (
              <article key={article.id} className="article-card">
                {article.image_url && (
                  <img src={article.image_url} alt={article.title} className="article-image" />
                )}
                <div className="article-content">
                  <h3>{article.title}</h3>
                  <p className="article-excerpt">{article.content.substring(0, 150)}...</p>
                  <div className="article-meta">
                    <span className="category">{article.category}</span>
                    <span className="views">👁️ {article.views}</span>
                  </div>
                  <div className="article-actions">
                    <Link to={`/article/${article.id}`} className="read-btn">
                      Read More
                    </Link>
                    <button
                      onClick={() => handleBookmark(article.id, article.is_bookmarked)}
                      className={`bookmark-btn ${article.is_bookmarked ? 'bookmarked' : ''}`}
                    >
                      {article.is_bookmarked ? '⭐' : '☆'}
                    </button>
                  </div>
                </div>
              </article>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default Home;

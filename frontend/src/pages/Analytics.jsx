import { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import '../styles/Analytics.css';

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await analyticsAPI.get();
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to load analytics', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  if (!analytics) {
    return <div className="error">Failed to load analytics</div>;
  }

  return (
    <div className="analytics">
      <h1>Platform Analytics</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Articles</h3>
          <p className="stat-value">{analytics.total_articles}</p>
        </div>

        <div className="stat-card">
          <h3>Total Users</h3>
          <p className="stat-value">{analytics.total_users}</p>
        </div>

        <div className="stat-card">
          <h3>Total Views</h3>
          <p className="stat-value">{analytics.total_views.toLocaleString()}</p>
        </div>
      </div>

      <div className="analytics-section">
        <h2>Articles by Category</h2>
        <div className="category-stats">
          {Object.entries(analytics.articles_by_category).map(([category, count]) => (
            <div key={category} className="category-item">
              <span className="category-name">{category}</span>
              <span className="category-count">{count}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="analytics-section">
        <h2>Top Articles</h2>
        <div className="top-articles">
          {analytics.top_articles.map((article, index) => (
            <div key={index} className="top-article-item">
              <span className="rank">#{index + 1}</span>
              <span className="title">{article.title}</span>
              <span className="views">👁️ {article.views}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Analytics;

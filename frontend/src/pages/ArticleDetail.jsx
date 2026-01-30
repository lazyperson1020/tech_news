import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { articlesAPI, bookmarksAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import '../styles/ArticleDetail.css';

function ArticleDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [summarizing, setSummarizing] = useState(false);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  useEffect(() => {
    loadArticle();
  }, [id]);

  const loadArticle = async () => {
    try {
      const response = await articlesAPI.getOne(id);
      setArticle(response.data);
      setIsBookmarked(response.data.is_bookmarked);
    } catch (error) {
      console.error('Failed to load article', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBookmark = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      if (isBookmarked) {
        await bookmarksAPI.remove(id);
      } else {
        await bookmarksAPI.create(id);
      }
      setIsBookmarked(!isBookmarked);
    } catch (error) {
      console.error('Bookmark action failed', error);
    }
  };

  const handleSummarize = async () => {
    setSummarizing(true);
    try {
      const response = await articlesAPI.summarize(id);
      setArticle({ ...article, summary: response.data.summary });
    } catch (error) {
      alert('Failed to generate summary');
    } finally {
      setSummarizing(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading article...</div>;
  }

  if (!article) {
    return <div className="error">Article not found</div>;
  }

  return (
    <div className="article-detail">
      <button onClick={() => navigate('/')} className="back-btn">
        ← Back to Articles
      </button>

      {article.image_url && (
        <img src={article.image_url} alt={article.title} className="article-hero-image" />
      )}

      <article className="article-body">
        <h1>{article.title}</h1>

        <div className="article-header">
          <div className="article-info">
            <span className="category">{article.category}</span>
            <span className="source">{article.source}</span>
            <span className="views">👁️ {article.views} views</span>
          </div>

          <div className="article-actions">
            {isAuthenticated && (
              <>
                <button
                  onClick={handleBookmark}
                  className={`bookmark-btn ${isBookmarked ? 'bookmarked' : ''}`}
                >
                  {isBookmarked ? '⭐ Bookmarked' : '☆ Bookmark'}
                </button>
                <button
                  onClick={handleSummarize}
                  disabled={summarizing || article.summary}
                  className="summarize-btn"
                >
                  {summarizing ? 'Generating...' : 'AI Summary'}
                </button>
              </>
            )}
          </div>
        </div>

        {article.author_name && (
          <p className="article-author">By {article.author_name}</p>
        )}

        {article.summary && (
          <div className="summary-box">
            <h3>📝 Summary</h3>
            <p>{article.summary}</p>
          </div>
        )}

        <div className="article-content">
          {article.content}
        </div>

        {article.source_url && (
          <a href={article.source_url} target="_blank" rel="noopener noreferrer" className="source-link">
            Read original article →
          </a>
        )}
      </article>
    </div>
  );
}

export default ArticleDetail;

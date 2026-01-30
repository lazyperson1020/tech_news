import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { bookmarksAPI } from '../services/api';
import '../styles/Bookmarks.css';

function Bookmarks() {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    try {
      const response = await bookmarksAPI.getAll();
      setBookmarks(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to load bookmarks', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveBookmark = async (articleId) => {
    try {
      await bookmarksAPI.remove(articleId);
      setBookmarks(bookmarks.filter((b) => b.article.id !== articleId));
    } catch (error) {
      console.error('Failed to remove bookmark', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading bookmarks...</div>;
  }

  return (
    <div className="bookmarks">
      <h1>My Bookmarks</h1>

      {bookmarks.length === 0 ? (
        <p className="no-bookmarks">You haven't bookmarked any articles yet</p>
      ) : (
        <div className="bookmarks-list">
          {bookmarks.map((bookmark) => (
            <article key={bookmark.id} className="bookmark-item">
              <h3>{bookmark.article.title}</h3>
              <p className="bookmark-excerpt">
                {bookmark.article.content.substring(0, 200)}...
              </p>
              <div className="bookmark-footer">
                <Link to={`/article/${bookmark.article.id}`} className="read-link">
                  Read Article
                </Link>
                <button
                  onClick={() => handleRemoveBookmark(bookmark.article.id)}
                  className="remove-btn"
                >
                  Remove
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default Bookmarks;

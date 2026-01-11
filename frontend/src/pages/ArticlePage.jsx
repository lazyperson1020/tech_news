import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { articleService } from '../services/articleService';
import { useAuth } from '../context/AuthContext';
import Loader from '../components/common/Loader';

const ArticlePage = () => {
  const { slug } = useParams();
  const { isAuthenticated } = useAuth();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generatingSummary, setGeneratingSummary] = useState(false);

  useEffect(() => {
    fetchArticle();
  }, [slug]);

  const fetchArticle = async () => {
    try {
      const data = await articleService.getArticle(slug);
      setArticle(data);
    } catch (error) {
      console.error('Error fetching article:', error);
      // Set demo article if API not available
      setArticle({
        id: 1,
        slug: slug,
        title: 'Demo Article - Backend Not Available',
        excerpt: 'This is a demo article. Connect the backend server to load real articles.',
        content: '<p>Please ensure your Django backend is running on <code>http://localhost:8000</code></p>',
        featured_image: 'https://via.placeholder.com/800x400',
        author: { username: 'demo_user' },
        published_at: new Date().toISOString(),
        reading_time: 5,
        views_count: 100,
        likes_count: 10,
        bookmarks_count: 2,
        categories: [],
        tags: ['demo', 'article'],
        source_url: null,
        source_name: null,
        is_bookmarked: false,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSummary = async () => {
    if (!isAuthenticated) {
      alert('Please login to generate summaries');
      return;
    }

    try {
      setGeneratingSummary(true);
      const data = await articleService.generateSummary(slug);
      setArticle({ ...article, summary: data.summary });
    } catch (error) {
      console.error('Error generating summary:', error);
      alert('Failed to generate summary');
    } finally {
      setGeneratingSummary(false);
    }
  };

  const handleLike = async () => {
    if (!isAuthenticated) {
      alert('Please login to like articles');
      return;
    }

    try {
      const data = await articleService.likeArticle(slug);
      setArticle({ ...article, likes_count: data.likes_count });
    } catch (error) {
      console.error('Error liking article:', error);
    }
  };

  const handleBookmark = async () => {
    if (!isAuthenticated) {
      alert('Please login to bookmark articles');
      return;
    }

    try {
      if (article.is_bookmarked) {
        alert('Bookmark removed');
      } else {
        await articleService.addBookmark(article.id);
        setArticle({ ...article, is_bookmarked: true, bookmarks_count: article.bookmarks_count + 1 });
        alert('Article bookmarked!');
      }
    } catch (error) {
      console.error('Error bookmarking article:', error);
    }
  };

  if (loading) {
    return <Loader />;
  }

  if (!article) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Article not found</h1>
        <Link to="/" className="text-primary-600">Go back to home</Link>
      </div>
    );
  }

  return (
    <article className="max-w-4xl mx-auto">
      <div className="mb-6">
        <div className="mb-2 text-sm text-gray-500">
          {article.categories?.map((category) => (
            <span key={category.id} className="mr-2">{category.name}</span>
          ))}
        </div>

        <h1 className="text-4xl font-bold mb-4">{article.title}</h1>

        <div className="flex justify-between items-center mb-6 text-sm text-gray-600">
          <div>
            {article.author && (
              <span>By {article.author.username}</span>
            )}
            <span className="mx-2">•</span>
            <span>{new Date(article.published_at).toLocaleDateString()} • {article.reading_time} min read</span>
          </div>

          <div className="space-x-4">
            <button onClick={handleLike} className="hover:text-primary-600">
              ❤️ {article.likes_count}
            </button>
            <button onClick={handleBookmark} className="hover:text-primary-600">
              {article.is_bookmarked ? '📕' : '📚'} {article.bookmarks_count}
            </button>
          </div>
        </div>

        {article.featured_image && (
          <img src={article.featured_image} alt={article.title} className="w-full rounded-lg mb-6" />
        )}
      </div>

      {article.summary ? (
        <div className="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg mb-6 border border-blue-200 dark:border-blue-700">
          <h3 className="font-semibold mb-2">🤖 AI Summary</h3>
          <p>{article.summary}</p>
        </div>
      ) : (
        isAuthenticated && (
          <div className="mb-6">
            <p className="text-gray-600 mb-3">Generate an AI-powered summary of this article</p>
            <button
              onClick={handleGenerateSummary}
              className="btn-primary"
              disabled={generatingSummary}
            >
              {generatingSummary ? 'Generating...' : 'Generate Summary'}
            </button>
          </div>
        )
      )}

      <div className="prose dark:prose-invert max-w-none mb-6">
        <div dangerouslySetInnerHTML={{ __html: article.content }} />
      </div>

      {article.source_url && (
        <div className="my-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <a href={article.source_url} target="_blank" rel="noreferrer" className="text-primary-600">
            Read original article at {article.source_name} →
          </a>
        </div>
      )}

      {article.tags && article.tags.length > 0 && (
        <div className="mt-6">
          {article.tags.map((tag, index) => (
            <span key={index} className="inline-block bg-gray-200 dark:bg-gray-700 px-3 py-1 rounded-full text-sm mr-2 mb-2">
              #{tag}
            </span>
          ))}
        </div>
      )}
    </article>
  );
};

export default ArticlePage;
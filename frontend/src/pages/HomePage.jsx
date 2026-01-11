import React, { useState, useEffect, useCallback } from 'react';
import { articleService } from '../services/articleService';
import ArticleList from '../components/articles/ArticleList';

const HomePage = () => {
  const [articles, setArticles] = useState([]);
  const [featured, setFeatured] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [selectedCategory, fetchData]);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const params = selectedCategory ? { categories__slug: selectedCategory } : {};
      
      const [articlesData, featuredData, categoriesData] = await Promise.all([
        articleService.getArticles(params),
        articleService.getFeatured(),
        articleService.getCategories(),
      ]);

      setArticles(articlesData.results || articlesData);
      setFeatured(featuredData);
      setCategories(categoriesData.results || categoriesData);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Unable to load articles. Make sure the backend is running.');
      // Set demo data for development
      setArticles([
        {
          id: 1,
          slug: 'sample-article',
          title: 'Welcome to The Silicon Post',
          excerpt: 'This is a demo article. Connect the backend to load real articles.',
          featured_image: 'https://via.placeholder.com/400x250',
          author: { username: 'demo_user' },
          published_at: new Date().toISOString(),
          reading_time: 5,
          views_count: 100,
          likes_count: 10,
          bookmarks_count: 2,
        },
      ]);
      setCategories([
        { id: 1, slug: 'ai', name: '🤖 AI', icon: '🤖' },
        { id: 2, slug: 'blockchain', name: '⛓️ Blockchain', icon: '⛓️' },
        { id: 3, slug: 'security', name: '🔒 Security', icon: '🔒' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <section className="text-center py-12 mb-12">
        <h1 className="text-5xl font-bold mb-4">Latest Technology News</h1>
        <p className="text-xl text-gray-600 dark:text-gray-300">
          Stay updated with the latest trends in AI, blockchain, cybersecurity, and more.
        </p>
      </section>

      {error && (
        <div className="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 text-yellow-800 dark:text-yellow-100 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {featured.length > 0 && (
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6">Featured Articles</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {featured.slice(0, 2).map((article) => (
              <div key={article.id} className="card">
                {article.featured_image && (
                  <img src={article.featured_image} alt={article.title} className="w-full h-48 object-cover rounded-md mb-4" />
                )}
                <h3 className="text-xl font-semibold mb-2">{article.title}</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-4">{article.excerpt}</p>
                <a href={`/articles/${article.slug}`} className="text-primary-600 font-semibold">
                  Read More →
                </a>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="mb-12">
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => setSelectedCategory('')}
            className={`px-4 py-2 rounded-lg ${
              selectedCategory === ''
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700'
            }`}
          >
            All
          </button>
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.slug)}
              className={`px-4 py-2 rounded-lg ${
                selectedCategory === category.slug
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700'
              }`}
            >
              {category.icon} {category.name}
            </button>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-3xl font-bold mb-6">
          {selectedCategory ? `${selectedCategory} Articles` : 'All Articles'}
        </h2>
        <ArticleList articles={articles} loading={loading} />
      </section>
    </div>
  );
};

export default HomePage;
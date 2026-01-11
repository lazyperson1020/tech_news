
import React from 'react';
import { Link } from 'react-router-dom';

const ArticleCard = ({ article }) => {
  return (
    <article className="card">
      {article.featured_image && (
        <img src={article.featured_image} alt={article.title} className="w-full h-48 object-cover rounded-md mb-4" />
      )}

      <div className="mb-2 text-sm text-gray-500">
        {article.categories?.map((category) => (
          <span key={category.id} className="mr-2">{category.name}</span>
        ))}
      </div>

      <h3 className="text-lg font-semibold mb-2">
        <Link to={`/articles/${article.slug}`}>{article.title}</Link>
      </h3>

      <p className="text-gray-600 mb-4">{article.excerpt}</p>

      <div className="flex items-center justify-between text-sm text-gray-500">
        <div>
          👁️ {article.views_count} &nbsp; ❤️ {article.likes_count} &nbsp; 📚 {article.bookmarks_count}
        </div>
        <div>{article.reading_time || '—'} min read</div>
      </div>

      {article.author && (
        <div className="mt-4 text-sm text-gray-500">
          By {article.author.username} · {article.published_at ? new Date(article.published_at).toLocaleDateString() : ''}
        </div>
      )}
    </article>
  );
};

export default ArticleCard;
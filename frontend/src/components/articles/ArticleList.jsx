import React from 'react';
import ArticleCard from './ArticleCard';
import Loader from '../common/Loader';

const ArticleList = ({ articles, loading }) => {
  if (loading) {
    return <Loader />;
  }

  if (!articles || articles.length === 0) {
    return (
      <div className="p-6 text-center text-gray-500">No articles found</div>
    );
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {articles.map((article) => (
        <ArticleCard key={article.id || article.slug} article={article} />
      ))}
    </div>
  );
};

export default ArticleList;
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { articlesAPI } from '../services/api';
import '../styles/CreateArticle.css';

function CreateArticle() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category: 'general',
    image_url: '',
    source_url: '',
  });
  const [loading, setLoading] = useState(false);

  const categories = [
    { value: 'ai_ml', label: 'AI/ML' },
    { value: 'blockchain', label: 'Blockchain' },
    { value: 'web_dev', label: 'Web Development' },
    { value: 'app_dev', label: 'App Development' },
    { value: 'cybersecurity', label: 'Cybersecurity' },
    { value: 'cloud', label: 'Cloud Computing' },
    { value: 'general', label: 'General Tech' },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await articlesAPI.create(formData);
      alert('Article created successfully!');
      navigate('/');
    } catch (error) {
      alert('Failed to create article');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-article">
      <h1>Create New Article</h1>

      <form onSubmit={handleSubmit} className="article-form">
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder="Article title"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>Category</label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="form-input"
          >
            {categories.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Content</label>
          <textarea
            name="content"
            value={formData.content}
            onChange={handleChange}
            required
            placeholder="Write your article content here..."
            rows={15}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>Image URL (optional)</label>
          <input
            type="url"
            name="image_url"
            value={formData.image_url}
            onChange={handleChange}
            placeholder="https://example.com/image.jpg"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>Source URL (optional)</label>
          <input
            type="url"
            name="source_url"
            value={formData.source_url}
            onChange={handleChange}
            placeholder="https://example.com/article"
            className="form-input"
          />
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Publishing...' : 'Publish Article'}
        </button>
      </form>
    </div>
  );
}

export default CreateArticle;

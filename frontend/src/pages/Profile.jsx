import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import '../styles/Profile.css';

function Profile() {
  const { profile, updateProfile, logout } = useAuthStore();
  const navigate = useNavigate();
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    bio: '',
    h_index: 0,
    credentials: '',
    experience: '',
  });

  useEffect(() => {
    if (profile) {
      setFormData({
        bio: profile.bio || '',
        h_index: profile.h_index || 0,
        credentials: profile.credentials || '',
        experience: profile.experience || '',
      });
    }
  }, [profile]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'h_index' ? parseInt(value) : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await updateProfile(formData);
    if (success) {
      setEditing(false);
      alert('Profile updated successfully');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (!profile) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile">
      <div className="profile-header">
        <h1>{profile.user.username}</h1>
        <p>{profile.user.email}</p>
      </div>

      {editing ? (
        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-group">
            <label>Bio</label>
            <textarea
              name="bio"
              value={formData.bio}
              onChange={handleChange}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label>H-Index</label>
            <input
              type="number"
              name="h_index"
              value={formData.h_index}
              onChange={handleChange}
              min="0"
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label>Credentials</label>
            <input
              type="text"
              name="credentials"
              value={formData.credentials}
              onChange={handleChange}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label>Experience</label>
            <textarea
              name="experience"
              value={formData.experience}
              onChange={handleChange}
              rows={4}
              className="form-input"
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="save-btn">
              Save Changes
            </button>
            <button type="button" onClick={() => setEditing(false)} className="cancel-btn">
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div className="profile-view">
          <div className="profile-info">
            <p><strong>Bio:</strong> {profile.bio || 'No bio yet'}</p>
            <p><strong>H-Index:</strong> {profile.h_index}</p>
            <p><strong>Credentials:</strong> {profile.credentials || 'None'}</p>
            <p><strong>Experience:</strong> {profile.experience || 'None'}</p>
            <p><strong>Author:</strong> {profile.is_author ? 'Yes' : 'No'}</p>
          </div>

          <div className="profile-actions">
            <button onClick={() => setEditing(true)} className="edit-btn">
              Edit Profile
            </button>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile;

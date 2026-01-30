import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import '../styles/Navbar.css';

function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <img src="/logo.png" alt="Silicon Post Logo" className="logo-image" />
        </Link>

        <div className="nav-menu">
          <Link to="/" className="nav-link">
            Home
          </Link>

          {isAuthenticated ? (
            <>
              <Link to="/create" className="nav-link">
                ✍️ Write
              </Link>
              <Link to="/bookmarks" className="nav-link">
                ⭐ Bookmarks
              </Link>
              <Link to="/chat" className="nav-link">
                💬 Chat
              </Link>
              <Link to="/profile" className="nav-link">
                👤 {user?.username}
              </Link>
              {user?.is_staff && (
                <Link to="/analytics" className="nav-link">
                  📊 Analytics
                </Link>
              )}
              <button onClick={handleLogout} className="nav-btn logout-btn">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-btn">
                Login
              </Link>
              <Link to="/register" className="nav-btn primary">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

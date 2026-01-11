// ...existing code...
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { darkMode, toggleDarkMode } = useTheme();

  return (
    <nav className="bg-white dark:bg-gray-800 border-b">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to="/" className="text-xl font-bold">The Silicon Post</Link>
          <Link to="/" className="text-sm">Home</Link>
          <Link to="/trending" className="text-sm">Trending</Link>
          <Link to="/categories" className="text-sm">Categories</Link>
        </div>

        <div className="flex items-center gap-4">
          <button onClick={toggleDarkMode} className="px-2">{darkMode ? '🌞' : '🌙'}</button>

          {isAuthenticated ? (
            <>
              <Link to="/bookmarks" className="text-sm">📚 Bookmarks</Link>
              <span className="text-sm">{user?.username}</span>
              {user?.is_author && <Link to="/articles/create" className="text-sm">Write Article</Link>}
              <button onClick={logout} className="text-sm">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm">Login</Link>
              <Link to="/register" className="text-sm">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
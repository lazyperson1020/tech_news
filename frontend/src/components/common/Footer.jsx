import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-white dark:bg-gray-800 border-t mt-8">
      <div className="container mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div>
          <h3 className="text-xl font-bold">The Silicon Post</h3>
          <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">Your daily source for the latest technology news and insights.</p>
        </div>

        <div>
          <h4 className="font-semibold">Quick Links</h4>
          <ul className="mt-2 space-y-1">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/trending">Trending</Link></li>
            <li><Link to="/categories">Categories</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-semibold">Categories</h4>
          <ul className="mt-2 space-y-1 text-sm text-gray-600 dark:text-gray-300">
            <li>Artificial Intelligence</li>
            <li>Blockchain</li>
            <li>Cybersecurity</li>
          </ul>
        </div>

        <div>
          <h4 className="font-semibold">Connect</h4>
          <ul className="mt-2 space-y-1">
            <li><a href="https://twitter.com" target="_blank" rel="noreferrer">Twitter</a></li>
            <li><a href="https://www.linkedin.com" target="_blank" rel="noreferrer">LinkedIn</a></li>
            <li><a href="https://github.com" target="_blank" rel="noreferrer">GitHub</a></li>
          </ul>
        </div>
      </div>

      <div className="bg-gray-100 dark:bg-gray-900 text-center py-4 text-sm">© 2025 The Silicon Post. All rights reserved.</div>
    </footer>
  );
};

export default Footer;
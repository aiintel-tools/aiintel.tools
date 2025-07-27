import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">Product</h3>
            <ul className="space-y-2">
              <li><Link to="/tools" className="hover:text-blue-400">Browse Tools</Link></li>
              <li><Link to="/categories" className="hover:text-blue-400">Categories</Link></li>
              <li><Link to="/tools/featured" className="hover:text-blue-400">Featured Tools</Link></li>
              <li><Link to="/tools/new" className="hover:text-blue-400">New Tools</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Company</h3>
            <ul className="space-y-2">
              <li><Link to="/about" className="hover:text-blue-400">About Us</Link></li>
              <li><Link to="/contact" className="hover:text-blue-400">Contact</Link></li>
              <li><Link to="/blog" className="hover:text-blue-400">Blog</Link></li>
              <li><Link to="/careers" className="hover:text-blue-400">Careers</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Support</h3>
            <ul className="space-y-2">
              <li><Link to="/help" className="hover:text-blue-400">Help Center</Link></li>
              <li><Link to="/privacy" className="hover:text-blue-400">Privacy Policy</Link></li>
              <li><Link to="/terms" className="hover:text-blue-400">Terms of Service</Link></li>
              <li><Link to="/cookies" className="hover:text-blue-400">Cookie Policy</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Developers</h3>
            <ul className="space-y-2">
              <li><Link to="/api-docs" className="hover:text-blue-400">API Documentation</Link></li>
              <li><Link to="/submit-tool" className="hover:text-blue-400">Submit a Tool</Link></li>
              <li><Link to="/partner" className="hover:text-blue-400">Partner Program</Link></li>
              <li><Link to="/affiliate" className="hover:text-blue-400">Affiliate Program</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400">© 2025 AI Directory. All rights reserved.</p>
          <div className="mt-4 md:mt-0 flex space-x-6">
            <a href="https://cbbykhce.manus.space" target="_blank" rel="noopener noreferrer" className="text-gold-500 hover:text-gold-400 font-bold">Admin Portal</a>
            <Link to="/legal" className="text-gray-400 hover:text-white">Legal</Link>
            <Link to="/sitemap" className="text-gray-400 hover:text-white">Sitemap</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;


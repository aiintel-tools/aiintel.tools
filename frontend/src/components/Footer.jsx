import React from 'react';
import { Link } from 'react-router-dom';
import aiIntelLogo from '../assets/ai-intel-logo.png';

const Footer = () => {
  return (
    <footer>
      <div className="container">
        <div className="footer-grid">
          <div className="footer-column">
            <h3>Product</h3>
            <ul className="footer-links">
              <li><Link to="/tools">Browse Tools</Link></li>
              <li><Link to="/categories">Categories</Link></li>
              <li><Link to="/tools/featured">Featured Tools</Link></li>
              <li><Link to="/tools/new">New Tools</Link></li>
            </ul>
          </div>
          
          <div className="footer-column">
            <h3>Company</h3>
            <ul className="footer-links">
              <li><Link to="/about">About Us</Link></li>
              <li><Link to="/contact">Contact</Link></li>
              <li><Link to="/blog">Blog</Link></li>
              <li><Link to="/careers">Careers</Link></li>
            </ul>
          </div>
          
          <div className="footer-column">
            <h3>Support</h3>
            <ul className="footer-links">
              <li><Link to="/help">Help Center</Link></li>
              <li><Link to="/privacy">Privacy Policy</Link></li>
              <li><Link to="/terms">Terms of Service</Link></li>
              <li><Link to="/cookies">Cookie Policy</Link></li>
            </ul>
          </div>
          
          <div className="footer-column">
            <h3>Developers</h3>
            <ul className="footer-links">
              <li><Link to="/api-docs">API Documentation</Link></li>
              <li><Link to="/submit-tool">Submit a Tool</Link></li>
              <li><Link to="/partner">Partner Program</Link></li>
              <li><Link to="/affiliate">Affiliate Program</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>© 2025 A.I Intel. All rights reserved.</p>
          <div className="footer-bottom-links">
            <Link to="/admin" className="admin-link">Admin Portal</Link>
            <Link to="/legal">Legal</Link>
            <Link to="/sitemap">Sitemap</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;


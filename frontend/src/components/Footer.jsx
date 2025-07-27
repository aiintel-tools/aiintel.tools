import React from 'react'
import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>AI Directory</h3>
            <p>Find the perfect AI tool for your business</p>
          </div>
          
          <div className="footer-section">
            <h4>Product</h4>
            <ul>
              <li><Link to="/tools">Browse Tools</Link></li>
              <li><Link to="/tools?view=categories">Categories</Link></li>
              <li><Link to="/pricing">Pricing</Link></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Company</h4>
            <ul>
              <li><Link to="/about">About Us</Link></li>
              <li><Link to="/contact">Contact</Link></li>
              <li><Link to="/blog">Blog</Link></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Legal</h4>
            <ul>
              <li><Link to="/terms">Terms of Service</Link></li>
              <li><Link to="/privacy">Privacy Policy</Link></li>
              <li><Link to="/cookies">Cookie Policy</Link></li>
              <li><Link to="/admin/login" className="admin-link">Admin Portal</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2025 AI Directory. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer


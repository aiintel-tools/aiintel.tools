import React from 'react';
import { Link } from 'react-router-dom';
import aiIntelLogo from '../assets/ai-intel-logo.png';

const Header = () => {
  return (
    <header>
      <div className="container">
        <nav>
          <Link to="/" className="logo">
            <img src={aiIntelLogo} alt="A.I Intel Logo" />
            <span>A.I Intel</span>
          </Link>
          
          <ul className="nav-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/tools">Browse Tools</Link></li>
            <li><Link to="/pricing">Pricing</Link></li>
          </ul>
          
          <div className="auth-buttons">
            <Link to="/auth" className="btn btn-outline">Sign In</Link>
            <Link to="/auth?tab=register" className="btn btn-primary">Get Started</Link>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Header;


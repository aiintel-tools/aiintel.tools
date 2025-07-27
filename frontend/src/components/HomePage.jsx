import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1>Find the Perfect <span>AI Tool</span> for Your Business</h1>
          <p>
            Discover and compare over 250+ AI tools to boost your productivity, 
            creativity, and business growth. Trusted by 15,000+ professionals.
          </p>
          
          <div className="search-container">
            <input 
              type="text" 
              placeholder="Search for AI tools, categories, or use cases..." 
            />
            <button>Search</button>
          </div>
        </div>
      </section>
      
      {/* Stats Section */}
      <section className="stats">
        <div className="container">
          <div className="stats-container">
            <div className="stat-item">
              <h3>250+</h3>
              <p>AI Tools Listed</p>
            </div>
            <div className="stat-item">
              <h3>15,000+</h3>
              <p>Active Users</p>
            </div>
            <div className="stat-item">
              <h3>8,500+</h3>
              <p>User Reviews</p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Featured Tools Section */}
      <section className="featured-tools">
        <div className="container">
          <div className="section-header">
            <h2>Featured AI Tools</h2>
            <p>Explore the most popular and highly-rated AI tools in our directory</p>
          </div>
          
          <div className="tools-grid">
            {/* Tool Card 1 */}
            <div className="tool-card">
              <div className="tool-card-content">
                <span className="tool-card-category">Conversational AI</span>
                <h3>ChatGPT</h3>
                <div className="tool-card-rating">
                  ★★★★★ <span>4.8</span>
                </div>
                <p>
                  Advanced language model that can generate human-like text, 
                  answer questions, and assist with various tasks.
                </p>
                <div className="tool-card-footer">
                  <Link to="/tools/chatgpt" className="btn btn-outline">View Details</Link>
                </div>
              </div>
            </div>
            
            {/* Tool Card 2 */}
            <div className="tool-card">
              <div className="tool-card-content">
                <span className="tool-card-category">Image Generation</span>
                <h3>Midjourney</h3>
                <div className="tool-card-rating">
                  ★★★★★ <span>4.7</span>
                </div>
                <p>
                  AI art generator that creates stunning images from text 
                  descriptions using advanced machine learning.
                </p>
                <div className="tool-card-footer">
                  <Link to="/tools/midjourney" className="btn btn-outline">View Details</Link>
                </div>
              </div>
            </div>
            
            {/* Tool Card 3 */}
            <div className="tool-card">
              <div className="tool-card-content">
                <span className="tool-card-category">Code Assistant</span>
                <h3>GitHub Copilot</h3>
                <div className="tool-card-rating">
                  ★★★★★ <span>4.6</span>
                </div>
                <p>
                  AI pair programmer that helps you write code faster with 
                  suggestions based on comments and context.
                </p>
                <div className="tool-card-footer">
                  <Link to="/tools/github-copilot" className="btn btn-outline">View Details</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="cta-section" style={{
        backgroundColor: '#4f46e5',
        color: 'white',
        padding: '4rem 0',
        textAlign: 'center'
      }}>
        <div className="container">
          <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>
            Ready to find the perfect AI tools for your business?
          </h2>
          <p style={{ fontSize: '1.25rem', marginBottom: '2rem', maxWidth: '800px', margin: '0 auto 2rem' }}>
            Join thousands of professionals who use A.I Intel to discover, 
            compare, and implement the best AI tools for their needs.
          </p>
          <Link to="/auth?tab=register" className="btn btn-primary" style={{
            backgroundColor: 'white',
            color: '#4f46e5',
            padding: '0.75rem 2rem',
            fontSize: '1.125rem'
          }}>
            Get Started - It's Free
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;


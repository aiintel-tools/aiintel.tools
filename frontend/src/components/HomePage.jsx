import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  const [tools, setTools] = useState([]);
  const [stats, setStats] = useState({
    users: 15000,
    tools: 250,
    reviews: 8500
  });

  useEffect(() => {
    // Fetch tools from API
    fetch('https://aiinteltools-production.up.railway.app/api/tools')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setTools(data.data.tools.slice(0, 3)); // Get first 3 tools for featured section
          setStats(prev => ({ ...prev, tools: data.data.tools.length }));
        }
      })
      .catch(error => {
        console.error('Error fetching tools:', error);
        // Fallback to static data if API fails
        setTools([
          {
            id: "1",
            name: "ChatGPT",
            description: "Advanced language model that can generate human-like text, answer questions, and assist with various tasks.",
            category: "Conversational AI",
            rating: 4.8
          },
          {
            id: "2", 
            name: "Midjourney",
            description: "AI art generator that creates stunning images from text descriptions using advanced machine learning.",
            category: "Image Generation",
            rating: 4.7
          },
          {
            id: "3",
            name: "GitHub Copilot", 
            description: "AI pair programmer that helps you write code faster with suggestions based on comments and context.",
            category: "Code Assistant",
            rating: 4.6
          }
        ]);
      });

    // Fetch user count
    fetch('https://aiinteltools-production.up.railway.app/api/users')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setStats(prev => ({ ...prev, users: data.data.users.length }));
        }
      })
      .catch(error => console.error('Error fetching users:', error));
  }, []);

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
              <h3>{stats.tools}+</h3>
              <p>AI Tools Listed</p>
            </div>
            <div className="stat-item">
              <h3>{stats.users}+</h3>
              <p>Active Users</p>
            </div>
            <div className="stat-item">
              <h3>{stats.reviews}+</h3>
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
            {tools.map((tool, index) => (
              <div key={tool.id} className="tool-card">
                <div className="tool-card-content">
                  <span className="tool-card-category">{tool.category}</span>
                  <h3>{tool.name}</h3>
                  <div className="tool-card-rating">
                    ★★★★★ <span>{tool.rating}</span>
                  </div>
                  <p>{tool.description}</p>
                  <div className="tool-card-footer">
                    <Link to={`/tools/${tool.name.toLowerCase().replace(/\s+/g, '-')}`} className="btn btn-outline">View Details</Link>
                  </div>
                </div>
              </div>
            ))}
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


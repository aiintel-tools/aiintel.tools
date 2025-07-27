import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const ToolsPage = () => {
  const [viewMode, setViewMode] = useState('grid')
  const [tools, setTools] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    // Fetch tools from API
    fetch('https://aiinteltools-production.up.railway.app/api/tools')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setTools(data.data.tools)
        }
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching tools:', error)
        // Fallback to static data if API fails
        setTools([
          {
            id: 1,
            name: 'ChatGPT',
            category: 'Conversational AI',
            description: 'Advanced AI chatbot for conversations and content creation',
            rating: 4.8
          },
          {
            id: 2,
            name: 'Midjourney',
            category: 'Image Generation',
            description: 'AI-powered image generation from text prompts',
            rating: 4.7
          },
          {
            id: 3,
            name: 'GitHub Copilot',
            category: 'Code Assistant',
            description: 'AI pair programmer that helps you write code faster',
            rating: 4.6
          }
        ])
        setLoading(false)
      })
  }, [])

  return (
    <div className="tools-page">
      <div className="container">
        <div className="page-header">
          <h1>AI Tools Directory</h1>
          <p>Discover and explore the best AI tools for your business needs</p>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <p>Loading tools...</p>
          </div>
        ) : (
        
        <div className="tools-controls">
          <div className="search-container">
            <input 
              type="text" 
              placeholder="Search tools..." 
              className="search-input"
            />
          </div>
          
          <div className="view-controls">
            <button 
              className={`view-button ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
            >
              Grid
            </button>
            <button 
              className={`view-button ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
            >
              List
            </button>
          </div>
        </div>
        
        <div className="tools-container">
          <div className="filters">
            <h3>Filters</h3>
            
            <div className="filter-group">
              <h4>Categories</h4>
              <div className="filter-options">
                <label>
                  <input type="checkbox" /> Conversational AI
                </label>
                <label>
                  <input type="checkbox" /> Image Generation
                </label>
                <label>
                  <input type="checkbox" /> Code Assistant
                </label>
                <label>
                  <input type="checkbox" /> Data Analysis
                </label>
                <label>
                  <input type="checkbox" /> Content Creation
                </label>
              </div>
            </div>
            
            <div className="filter-group">
              <h4>Pricing</h4>
              <div className="filter-options">
                <label>
                  <input type="checkbox" /> Free
                </label>
                <label>
                  <input type="checkbox" /> Freemium
                </label>
                <label>
                  <input type="checkbox" /> Paid
                </label>
              </div>
            </div>
            
            <div className="filter-group">
              <h4>Rating</h4>
              <div className="filter-options">
                <label>
                  <input type="checkbox" /> 4+ Stars
                </label>
                <label>
                  <input type="checkbox" /> 3+ Stars
                </label>
              </div>
            </div>
            
            <button className="clear-filters">Clear Filters</button>
          </div>
          
          <div className={`tools-list ${viewMode}`}>
            {tools.map(tool => (
              <div key={tool.id} className="tool-card">
                <div className="tool-category">{tool.category}</div>
                <h3>{tool.name}</h3>
                <p>{tool.description}</p>
                <div className="tool-rating">
                  <span className="stars">★★★★★</span>
                  <span className="rating-value">{tool.rating}</span>
                </div>
                <Link to={`/tools/${tool.id}`} className="view-details">
                  View Details
                </Link>
              </div>
            ))}
          </div>
        </div>
        )}
      </div>
    </div>
  )
}

export default ToolsPage


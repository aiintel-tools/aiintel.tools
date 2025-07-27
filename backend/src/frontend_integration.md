# AI Directory Platform - Frontend Integration

## Overview

This document outlines how the frontend components of the AI Directory Platform will integrate with the backend API. It covers the shared data layer approach, authentication flow, and specific integration points for the admin portal and tools manager.

## Shared Data Layer Architecture

The shared data layer will ensure that data is consistent across all frontend components of the platform. This will be implemented using a combination of API calls and local state management.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Applications                       │
├───────────────────┬───────────────────┬───────────────────┬─────┤
│  Main Website     │  Admin Dashboard  │  Tools Manager    │ ... │
├───────────────────┴───────────────────┴───────────────────┴─────┤
│                      Shared API Service Layer                    │
├─────────────────────────────────────────────────────────────────┤
│                      Authentication Service                      │
├─────────────────────────────────────────────────────────────────┤
│                         REST API Client                          │
├─────────────────────────────────────────────────────────────────┤
│                      Backend API (Flask)                         │
├─────────────────────────────────────────────────────────────────┤
│                      Database (SQLite)                           │
└─────────────────────────────────────────────────────────────────┘
```

## Shared API Service Layer

The shared API service layer will be implemented as a set of JavaScript modules that can be imported by any frontend component. This layer will handle all communication with the backend API, including authentication, error handling, and data transformation.

### Core API Service

```javascript
// api.js - Core API service

const API_BASE_URL = 'https://api.aidirectory.com/api/v1';

// Get the authentication token from localStorage
const getToken = () => localStorage.getItem('auth_token');

// Set the authentication token in localStorage
const setToken = (token) => localStorage.setItem('auth_token', token);

// Remove the authentication token from localStorage
const removeToken = () => localStorage.removeItem('auth_token');

// Check if the user is authenticated
const isAuthenticated = () => !!getToken();

// Make an API request
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Set default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  // Add authentication token if available
  if (isAuthenticated()) {
    headers['Authorization'] = `Bearer ${getToken()}`;
  }
  
  // Make the request
  try {
    const response = await fetch(url, {
      ...options,
      headers
    });
    
    // Parse the response
    const data = await response.json();
    
    // Check for errors
    if (!response.ok) {
      throw {
        status: response.status,
        ...data
      };
    }
    
    return data;
  } catch (error) {
    // Handle token expiration
    if (error.status === 401 && isAuthenticated()) {
      // Try to refresh the token
      try {
        const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${getToken()}`
          }
        });
        
        const refreshData = await refreshResponse.json();
        
        if (refreshResponse.ok && refreshData.data.token) {
          // Update the token
          setToken(refreshData.data.token);
          
          // Retry the original request
          return apiRequest(endpoint, options);
        } else {
          // If refresh fails, log out the user
          removeToken();
          window.location.href = '/login';
        }
      } catch (refreshError) {
        // If refresh fails, log out the user
        removeToken();
        window.location.href = '/login';
      }
    }
    
    // Re-throw the error for the caller to handle
    throw error;
  }
};

// API methods
export default {
  // Authentication
  auth: {
    login: (email, password) => apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    }),
    register: (userData) => apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    }),
    logout: () => {
      removeToken();
      return Promise.resolve();
    }
  },
  
  // Users
  users: {
    me: () => apiRequest('/users/me'),
    update: (userData) => apiRequest('/users/me', {
      method: 'PUT',
      body: JSON.stringify(userData)
    }),
    list: (params) => apiRequest(`/users?${new URLSearchParams(params)}`),
    get: (id) => apiRequest(`/users/${id}`),
    update: (id, userData) => apiRequest(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData)
    }),
    delete: (id) => apiRequest(`/users/${id}`, {
      method: 'DELETE'
    })
  },
  
  // AI Tools
  tools: {
    list: (params) => apiRequest(`/tools?${new URLSearchParams(params)}`),
    get: (id) => apiRequest(`/tools/${id}`),
    create: (toolData) => {
      // Handle file uploads
      const formData = new FormData();
      
      // Add all fields to the form data
      Object.keys(toolData).forEach(key => {
        if (key === 'image' && toolData[key] instanceof File) {
          formData.append('image', toolData[key]);
        } else if (key === 'industry_ids' && Array.isArray(toolData[key])) {
          toolData[key].forEach(id => formData.append('industry_ids', id));
        } else {
          formData.append(key, toolData[key]);
        }
      });
      
      return apiRequest('/tools', {
        method: 'POST',
        headers: {}, // Let the browser set the Content-Type for multipart/form-data
        body: formData
      });
    },
    update: (id, toolData) => {
      // Handle file uploads
      const formData = new FormData();
      
      // Add all fields to the form data
      Object.keys(toolData).forEach(key => {
        if (key === 'image' && toolData[key] instanceof File) {
          formData.append('image', toolData[key]);
        } else if (key === 'industry_ids' && Array.isArray(toolData[key])) {
          toolData[key].forEach(id => formData.append('industry_ids', id));
        } else {
          formData.append(key, toolData[key]);
        }
      });
      
      return apiRequest(`/tools/${id}`, {
        method: 'PUT',
        headers: {}, // Let the browser set the Content-Type for multipart/form-data
        body: formData
      });
    },
    delete: (id) => apiRequest(`/tools/${id}`, {
      method: 'DELETE'
    })
  },
  
  // Categories
  categories: {
    list: () => apiRequest('/categories'),
    create: (categoryData) => apiRequest('/categories', {
      method: 'POST',
      body: JSON.stringify(categoryData)
    }),
    update: (id, categoryData) => apiRequest(`/categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(categoryData)
    }),
    delete: (id) => apiRequest(`/categories/${id}`, {
      method: 'DELETE'
    })
  },
  
  // Industries
  industries: {
    list: () => apiRequest('/industries'),
    create: (industryData) => apiRequest('/industries', {
      method: 'POST',
      body: JSON.stringify(industryData)
    }),
    update: (id, industryData) => apiRequest(`/industries/${id}`, {
      method: 'PUT',
      body: JSON.stringify(industryData)
    }),
    delete: (id) => apiRequest(`/industries/${id}`, {
      method: 'DELETE'
    })
  },
  
  // Reviews
  reviews: {
    list: (toolId, params) => apiRequest(`/tools/${toolId}/reviews?${new URLSearchParams(params)}`),
    create: (toolId, reviewData) => apiRequest(`/tools/${toolId}/reviews`, {
      method: 'POST',
      body: JSON.stringify(reviewData)
    }),
    update: (id, reviewData) => apiRequest(`/reviews/${id}`, {
      method: 'PUT',
      body: JSON.stringify(reviewData)
    }),
    delete: (id) => apiRequest(`/reviews/${id}`, {
      method: 'DELETE'
    }),
    verify: (id) => apiRequest(`/reviews/${id}/verify`, {
      method: 'PUT'
    })
  },
  
  // Favorites
  favorites: {
    list: (params) => apiRequest(`/users/me/favorites?${new URLSearchParams(params)}`),
    add: (toolId) => apiRequest(`/tools/${toolId}/favorite`, {
      method: 'POST'
    }),
    remove: (toolId) => apiRequest(`/tools/${toolId}/favorite`, {
      method: 'DELETE'
    })
  },
  
  // Subscriptions
  subscriptions: {
    plans: () => apiRequest('/subscriptions/plans'),
    subscribe: (planData) => apiRequest('/subscriptions/subscribe', {
      method: 'POST',
      body: JSON.stringify(planData)
    }),
    current: () => apiRequest('/subscriptions/me'),
    cancel: (cancelData) => apiRequest('/subscriptions/cancel', {
      method: 'POST',
      body: JSON.stringify(cancelData)
    })
  },
  
  // Admin Dashboard
  admin: {
    dashboard: () => apiRequest('/admin/dashboard')
  }
};
```

## Authentication Integration

The authentication service will be used by all frontend components to handle user authentication and authorization.

### Authentication Context

```jsx
// AuthContext.jsx - Authentication context for React components

import React, { createContext, useState, useEffect, useContext } from 'react';
import api from './api';

// Create the context
const AuthContext = createContext();

// Authentication provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Load the user on initial render
  useEffect(() => {
    const loadUser = async () => {
      try {
        // Check if we have a token
        if (api.isAuthenticated()) {
          // Get the current user
          const response = await api.users.me();
          setUser(response.data);
        }
      } catch (error) {
        console.error('Failed to load user:', error);
        // Clear the token if it's invalid
        api.auth.logout();
      } finally {
        setLoading(false);
      }
    };
    
    loadUser();
  }, []);
  
  // Login function
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.auth.login(email, password);
      
      // Save the token
      api.setToken(response.data.token);
      
      // Set the user
      setUser(response.data);
      
      return response.data;
    } catch (error) {
      setError(error.error?.message || 'Failed to login');
      throw error;
    } finally {
      setLoading(false);
    }
  };
  
  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.auth.register(userData);
      
      // Save the token
      api.setToken(response.data.token);
      
      // Set the user
      setUser(response.data);
      
      return response.data;
    } catch (error) {
      setError(error.error?.message || 'Failed to register');
      throw error;
    } finally {
      setLoading(false);
    }
  };
  
  // Logout function
  const logout = () => {
    api.auth.logout();
    setUser(null);
  };
  
  // Update user function
  const updateUser = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.users.update(userData);
      
      // Update the user
      setUser(response.data);
      
      return response.data;
    } catch (error) {
      setError(error.error?.message || 'Failed to update user');
      throw error;
    } finally {
      setLoading(false);
    }
  };
  
  // Check if the user is an admin
  const isAdmin = () => {
    return user && user.is_admin;
  };
  
  // Context value
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    updateUser,
    isAdmin
  };
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};
```

## Admin Portal Integration

The admin portal will use the shared API service to manage users, AI tools, categories, industries, and subscriptions.

### Admin Dashboard Component

```jsx
// AdminDashboard.jsx - Admin dashboard component

import React, { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import api from './api';

const AdminDashboard = () => {
  const { user, isAdmin } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Load dashboard stats on initial render
  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await api.admin.dashboard();
        setStats(response.data);
      } catch (error) {
        console.error('Failed to load dashboard stats:', error);
        setError(error.error?.message || 'Failed to load dashboard stats');
      } finally {
        setLoading(false);
      }
    };
    
    if (isAdmin()) {
      loadStats();
    }
  }, [isAdmin]);
  
  // Render loading state
  if (loading) {
    return <div>Loading dashboard...</div>;
  }
  
  // Render error state
  if (error) {
    return <div>Error: {error}</div>;
  }
  
  // Render unauthorized state
  if (!isAdmin()) {
    return <div>You are not authorized to access this page.</div>;
  }
  
  // Render dashboard
  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      
      {/* Stats cards */}
      <div className="stats-cards">
        <div className="stats-card">
          <h2>Users</h2>
          <div className="stats-value">{stats.users.total}</div>
          <div className="stats-growth">
            +{stats.users.new_this_month} this month ({stats.users.growth_percentage}%)
          </div>
        </div>
        
        <div className="stats-card">
          <h2>AI Tools</h2>
          <div className="stats-value">{stats.tools.total}</div>
          <div className="stats-growth">
            +{stats.tools.new_this_month} this month ({stats.tools.growth_percentage}%)
          </div>
        </div>
        
        <div className="stats-card">
          <h2>Reviews</h2>
          <div className="stats-value">{stats.reviews.total}</div>
          <div className="stats-growth">
            +{stats.reviews.new_this_month} this month ({stats.reviews.growth_percentage}%)
          </div>
        </div>
        
        <div className="stats-card">
          <h2>Revenue</h2>
          <div className="stats-value">${stats.revenue.total_monthly}</div>
          <div className="stats-growth">
            +{stats.revenue.growth_percentage}% this month
          </div>
        </div>
      </div>
      
      {/* Popular tools */}
      <div className="popular-tools">
        <h2>Popular Tools</h2>
        <table>
          <thead>
            <tr>
              <th>Tool</th>
              <th>Views</th>
              <th>Favorites</th>
              <th>Reviews</th>
            </tr>
          </thead>
          <tbody>
            {stats.popular_tools.map(tool => (
              <tr key={tool.id}>
                <td>{tool.name}</td>
                <td>{tool.views}</td>
                <td>{tool.favorites}</td>
                <td>{tool.reviews}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Recent activities */}
      <div className="recent-activities">
        <h2>Recent Activities</h2>
        <ul>
          {stats.recent_activities.map(activity => (
            <li key={activity.id}>
              {activity.type === 'new_user' && (
                <span>
                  New user: {activity.user.first_name} {activity.user.last_name}
                </span>
              )}
              <span className="activity-time">
                {new Date(activity.created_at).toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AdminDashboard;
```

## AI Tools Manager Integration

The AI Tools Manager will use the shared API service to manage AI tools, including creating, updating, and deleting tools, as well as setting access levels.

### AI Tools Manager Component

```jsx
// ToolsManager.jsx - AI Tools Manager component

import React, { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import api from './api';

const ToolsManager = () => {
  const { isAdmin } = useAuth();
  const [tools, setTools] = useState([]);
  const [categories, setCategories] = useState([]);
  const [industries, setIndustries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTool, setSelectedTool] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category_id: '',
    website_url: '',
    access_level: 'Public',
    image: null,
    industry_ids: []
  });
  
  // Load tools, categories, and industries on initial render
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Load tools
        const toolsResponse = await api.tools.list();
        setTools(toolsResponse.data.tools);
        
        // Load categories
        const categoriesResponse = await api.categories.list();
        setCategories(categoriesResponse.data);
        
        // Load industries
        const industriesResponse = await api.industries.list();
        setIndustries(industriesResponse.data);
      } catch (error) {
        console.error('Failed to load data:', error);
        setError(error.error?.message || 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, []);
  
  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  // Handle checkbox changes for industries
  const handleIndustryChange = (e) => {
    const { value, checked } = e.target;
    const industryId = parseInt(value);
    
    setFormData(prev => {
      if (checked) {
        return {
          ...prev,
          industry_ids: [...prev.industry_ids, industryId]
        };
      } else {
        return {
          ...prev,
          industry_ids: prev.industry_ids.filter(id => id !== industryId)
        };
      }
    });
  };
  
  // Handle file input changes
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFormData(prev => ({ ...prev, image: file }));
  };
  
  // Open the modal for creating a new tool
  const openCreateModal = () => {
    setSelectedTool(null);
    setFormData({
      name: '',
      description: '',
      category_id: categories.length > 0 ? categories[0].id.toString() : '',
      website_url: '',
      access_level: 'Public',
      image: null,
      industry_ids: []
    });
    setIsModalOpen(true);
  };
  
  // Open the modal for editing an existing tool
  const openEditModal = (tool) => {
    setSelectedTool(tool);
    setFormData({
      name: tool.name,
      description: tool.description,
      category_id: tool.category.id.toString(),
      website_url: tool.website_url || '',
      access_level: tool.access_level,
      image: null,
      industry_ids: tool.industries.map(industry => industry.id)
    });
    setIsModalOpen(true);
  };
  
  // Close the modal
  const closeModal = () => {
    setIsModalOpen(false);
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      if (selectedTool) {
        // Update existing tool
        const response = await api.tools.update(selectedTool.id, formData);
        
        // Update the tools list
        setTools(prev => prev.map(tool => 
          tool.id === selectedTool.id ? response.data : tool
        ));
      } else {
        // Create new tool
        const response = await api.tools.create(formData);
        
        // Add the new tool to the list
        setTools(prev => [...prev, response.data]);
      }
      
      // Close the modal
      closeModal();
    } catch (error) {
      console.error('Failed to save tool:', error);
      setError(error.error?.message || 'Failed to save tool');
    } finally {
      setLoading(false);
    }
  };
  
  // Handle tool deletion
  const handleDelete = async (toolId) => {
    if (!window.confirm('Are you sure you want to delete this tool?')) {
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      await api.tools.delete(toolId);
      
      // Remove the tool from the list
      setTools(prev => prev.filter(tool => tool.id !== toolId));
    } catch (error) {
      console.error('Failed to delete tool:', error);
      setError(error.error?.message || 'Failed to delete tool');
    } finally {
      setLoading(false);
    }
  };
  
  // Render loading state
  if (loading && tools.length === 0) {
    return <div>Loading tools...</div>;
  }
  
  // Render error state
  if (error && tools.length === 0) {
    return <div>Error: {error}</div>;
  }
  
  // Render unauthorized state
  if (!isAdmin()) {
    return <div>You are not authorized to access this page.</div>;
  }
  
  // Render tools manager
  return (
    <div className="tools-manager">
      <h1>AI Tools Manager</h1>
      
      {/* Error message */}
      {error && <div className="error-message">{error}</div>}
      
      {/* Add tool button */}
      <button onClick={openCreateModal}>Add New Tool</button>
      
      {/* Tools table */}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Rating</th>
            <th>Access Level</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tools.map(tool => (
            <tr key={tool.id}>
              <td>{tool.name}</td>
              <td>{tool.category.name}</td>
              <td>{tool.rating}</td>
              <td>
                <span className={`access-level access-level-${tool.access_level.toLowerCase().replace(' ', '-')}`}>
                  {tool.access_level}
                </span>
              </td>
              <td>
                <button onClick={() => openEditModal(tool)}>Edit</button>
                <button onClick={() => handleDelete(tool.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* Tool modal */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>{selectedTool ? 'Edit AI Tool' : 'Add New AI Tool'}</h2>
              <button onClick={closeModal}>&times;</button>
            </div>
            <div className="modal-body">
              <form onSubmit={handleSubmit}>
                {/* Tool name */}
                <div className="form-group">
                  <label htmlFor="name">Tool Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                {/* Category */}
                <div className="form-group">
                  <label htmlFor="category_id">Category</label>
                  <select
                    id="category_id"
                    name="category_id"
                    value={formData.category_id}
                    onChange={handleInputChange}
                    required
                  >
                    {categories.map(category => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                {/* Description */}
                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    required
                  ></textarea>
                </div>
                
                {/* Website URL */}
                <div className="form-group">
                  <label htmlFor="website_url">Website URL</label>
                  <input
                    type="url"
                    id="website_url"
                    name="website_url"
                    value={formData.website_url}
                    onChange={handleInputChange}
                  />
                </div>
                
                {/* Access level */}
                <div className="form-group">
                  <label htmlFor="access_level">Access Level</label>
                  <select
                    id="access_level"
                    name="access_level"
                    value={formData.access_level}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="Public">Public (Free Access)</option>
                    <option value="Premium Only">Premium Only</option>
                    <option value="Business Only">Business Only</option>
                  </select>
                </div>
                
                {/* Tool image */}
                <div className="form-group">
                  <label htmlFor="image">Tool Image</label>
                  <div className="file-upload">
                    <input
                      type="file"
                      id="image"
                      name="image"
                      accept="image/*"
                      onChange={handleFileChange}
                    />
                    <div className="file-upload-label">
                      {formData.image ? formData.image.name : 'Click to upload image or drag and drop'}
                    </div>
                  </div>
                  <div className="help-text">
                    Recommended size: 400x400px. Max size: 2MB.
                  </div>
                  {selectedTool && selectedTool.image_url && (
                    <div className="current-image">
                      <img src={selectedTool.image_url} alt={selectedTool.name} />
                      <div>Current image</div>
                    </div>
                  )}
                </div>
                
                {/* Industries */}
                <div className="form-group">
                  <label>Industries</label>
                  {industries.map(industry => (
                    <div key={industry.id} className="checkbox-group">
                      <input
                        type="checkbox"
                        id={`industry-${industry.id}`}
                        name="industry_ids"
                        value={industry.id}
                        checked={formData.industry_ids.includes(industry.id)}
                        onChange={handleIndustryChange}
                      />
                      <label htmlFor={`industry-${industry.id}`}>
                        {industry.name}
                      </label>
                    </div>
                  ))}
                </div>
                
                {/* Submit button */}
                <div className="form-actions">
                  <button type="button" onClick={closeModal}>Cancel</button>
                  <button type="submit" disabled={loading}>
                    {loading ? 'Saving...' : selectedTool ? 'Save Changes' : 'Save Tool'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ToolsManager;
```

## Main Application Integration

The main application will use the shared API service to display AI tools, handle user authentication, and manage user subscriptions.

### App Component

```jsx
// App.jsx - Main application component

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import ToolsPage from './components/ToolsPage';
import ToolDetailPage from './components/ToolDetailPage';
import CategoryPage from './components/CategoryPage';
import PricingPage from './components/PricingPage';
import AuthPage from './components/AuthPage';
import UserDashboard from './components/UserDashboard';
import AdminDashboard from './components/AdminDashboard';
import ToolsManager from './components/ToolsManager';
import './App.css';

// Protected route component
const ProtectedRoute = ({ children, requireAdmin = false }) => {
  const { user, loading, isAdmin } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/auth" />;
  }
  
  if (requireAdmin && !isAdmin()) {
    return <Navigate to="/" />;
  }
  
  return children;
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Header />
          <main className="main-content">
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<HomePage />} />
              <Route path="/tools" element={<ToolsPage />} />
              <Route path="/tools/:id" element={<ToolDetailPage />} />
              <Route path="/categories/:id" element={<CategoryPage />} />
              <Route path="/pricing" element={<PricingPage />} />
              <Route path="/auth" element={<AuthPage />} />
              
              {/* Protected routes */}
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <UserDashboard />
                </ProtectedRoute>
              } />
              
              {/* Admin routes */}
              <Route path="/admin" element={
                <ProtectedRoute requireAdmin={true}>
                  <AdminDashboard />
                </ProtectedRoute>
              } />
              <Route path="/admin/tools" element={
                <ProtectedRoute requireAdmin={true}>
                  <ToolsManager />
                </ProtectedRoute>
              } />
              
              {/* Fallback route */}
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
```

## Error Handling and Loading States

All components will implement consistent error handling and loading states to provide a good user experience.

### Error Handling Component

```jsx
// ErrorMessage.jsx - Error message component

import React from 'react';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="error-message">
      <div className="error-icon">⚠️</div>
      <div className="error-text">{message}</div>
      {onRetry && (
        <button className="error-retry" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
```

### Loading Component

```jsx
// LoadingSpinner.jsx - Loading spinner component

import React from 'react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <div className="loading-text">{message}</div>
    </div>
  );
};

export default LoadingSpinner;
```

## Offline Support

The application will implement basic offline support to handle cases where the backend API is temporarily unavailable.

### Offline Fallback

```jsx
// offlineFallback.js - Offline fallback data

export const offlineFallback = {
  tools: [
    {
      id: 1,
      name: 'ChatGPT',
      description: 'AI language model by OpenAI',
      category: {
        id: 1,
        name: 'Conversational AI'
      },
      website_url: 'https://chat.openai.com',
      image_url: '/images/chatgpt.jpg',
      access_level: 'Public',
      rating: 4.8,
      industries: [
        {
          id: 1,
          name: 'Technology'
        },
        {
          id: 4,
          name: 'Education'
        }
      ]
    },
    // More tools...
  ],
  categories: [
    {
      id: 1,
      name: 'Conversational AI',
      description: 'AI tools for natural language conversations',
      icon: 'chat-bubble',
      tool_count: 15
    },
    // More categories...
  ],
  industries: [
    {
      id: 1,
      name: 'Technology',
      description: 'Technology and software companies'
    },
    // More industries...
  ]
};

// Function to get offline fallback data
export const getOfflineFallback = (key) => {
  return offlineFallback[key] || null;
};
```

### API Service with Offline Support

```javascript
// Enhanced API request function with offline support
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Set default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  // Add authentication token if available
  if (isAuthenticated()) {
    headers['Authorization'] = `Bearer ${getToken()}`;
  }
  
  // Make the request
  try {
    const response = await fetch(url, {
      ...options,
      headers
    });
    
    // Parse the response
    const data = await response.json();
    
    // Check for errors
    if (!response.ok) {
      throw {
        status: response.status,
        ...data
      };
    }
    
    return data;
  } catch (error) {
    // Handle token expiration
    if (error.status === 401 && isAuthenticated()) {
      // Try to refresh the token
      try {
        const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${getToken()}`
          }
        });
        
        const refreshData = await refreshResponse.json();
        
        if (refreshResponse.ok && refreshData.data.token) {
          // Update the token
          setToken(refreshData.data.token);
          
          // Retry the original request
          return apiRequest(endpoint, options);
        } else {
          // If refresh fails, log out the user
          removeToken();
          window.location.href = '/login';
        }
      } catch (refreshError) {
        // If refresh fails, log out the user
        removeToken();
        window.location.href = '/login';
      }
    }
    
    // Check if this is a network error (offline)
    if (error.message === 'Failed to fetch' || !navigator.onLine) {
      console.warn('Network error, using offline fallback data');
      
      // Extract the resource type from the endpoint
      const resource = endpoint.split('/')[1];
      
      // Get offline fallback data
      const fallbackData = getOfflineFallback(resource);
      
      if (fallbackData) {
        return {
          success: true,
          data: fallbackData,
          offline: true
        };
      }
    }
    
    // Re-throw the error for the caller to handle
    throw error;
  }
};
```

## Conclusion

This frontend integration design provides a comprehensive approach to ensuring data consistency across all components of the AI Directory Platform. By implementing a shared API service layer, all frontend components will have access to the same data and functionality, eliminating the data persistence issues between the admin portal and tools manager.

The design also includes proper error handling, loading states, and offline support to provide a good user experience even when the backend API is temporarily unavailable.

This approach is production-ready and can be easily extended to support additional features in the future.


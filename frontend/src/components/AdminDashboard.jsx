import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const navigate = useNavigate();
  
  // Check if admin is authenticated
  useEffect(() => {
    const isAuthenticated = localStorage.getItem('adminAuthenticated') === 'true';
    if (!isAuthenticated) {
      navigate('/admin/login');
    }
  }, [navigate]);
  
  const handleLogout = () => {
    localStorage.removeItem('adminAuthenticated');
    navigate('/admin/login');
  };
  
  // Mock data
  const stats = {
    users: 15482,
    tools: 253,
    reviews: 8743,
    revenue: 12850
  };
  
  const recentUsers = [
    { id: 1, name: 'John Doe', email: 'john@example.com', date: '2025-07-22', subscription: 'Premium' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', date: '2025-07-21', subscription: 'Business' },
    { id: 3, name: 'Robert Johnson', email: 'robert@example.com', date: '2025-07-20', subscription: 'Free' }
  ];
  
  const recentTools = [
    { id: 1, name: 'ChatGPT', category: 'Conversational AI', status: 'Active', rating: 4.8 },
    { id: 2, name: 'Midjourney', category: 'Image Generation', status: 'Active', rating: 4.7 },
    { id: 3, name: 'GitHub Copilot', category: 'Code Assistant', status: 'Active', rating: 4.6 }
  ];

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <div className="container">
          <div className="admin-header-content">
            <h1>Admin Dashboard</h1>
            <button onClick={handleLogout} className="logout-button">Logout</button>
          </div>
        </div>
      </div>
      
      <div className="container">
        <div className="admin-content">
          <div className="admin-sidebar">
            <nav className="admin-nav">
              <button 
                className={`admin-nav-item ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
              <button 
                className={`admin-nav-item ${activeTab === 'users' ? 'active' : ''}`}
                onClick={() => setActiveTab('users')}
              >
                Users
              </button>
              <button 
                className={`admin-nav-item ${activeTab === 'tools' ? 'active' : ''}`}
                onClick={() => setActiveTab('tools')}
              >
                AI Tools
              </button>
              <button 
                className={`admin-nav-item ${activeTab === 'reviews' ? 'active' : ''}`}
                onClick={() => setActiveTab('reviews')}
              >
                Reviews
              </button>
              <button 
                className={`admin-nav-item ${activeTab === 'subscriptions' ? 'active' : ''}`}
                onClick={() => setActiveTab('subscriptions')}
              >
                Subscriptions
              </button>
              <button 
                className={`admin-nav-item ${activeTab === 'settings' ? 'active' : ''}`}
                onClick={() => setActiveTab('settings')}
              >
                Settings
              </button>
            </nav>
          </div>
          
          <div className="admin-main">
            {activeTab === 'overview' && (
              <div className="admin-overview">
                <h2>Dashboard Overview</h2>
                
                <div className="stats-grid">
                  <div className="stat-card">
                    <h3>Total Users</h3>
                    <p className="stat-value">{stats.users.toLocaleString()}</p>
                    <p className="stat-change positive">+12% this month</p>
                  </div>
                  
                  <div className="stat-card">
                    <h3>AI Tools</h3>
                    <p className="stat-value">{stats.tools.toLocaleString()}</p>
                    <p className="stat-change positive">+5 this week</p>
                  </div>
                  
                  <div className="stat-card">
                    <h3>Reviews</h3>
                    <p className="stat-value">{stats.reviews.toLocaleString()}</p>
                    <p className="stat-change positive">+8% this month</p>
                  </div>
                  
                  <div className="stat-card">
                    <h3>Monthly Revenue</h3>
                    <p className="stat-value">${stats.revenue.toLocaleString()}</p>
                    <p className="stat-change positive">+15% this month</p>
                  </div>
                </div>
                
                <div className="admin-panels">
                  <div className="admin-panel">
                    <div className="panel-header">
                      <h3>Recent Users</h3>
                      <button className="view-all-button">View All</button>
                    </div>
                    
                    <table className="admin-table">
                      <thead>
                        <tr>
                          <th>Name</th>
                          <th>Email</th>
                          <th>Joined</th>
                          <th>Subscription</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recentUsers.map(user => (
                          <tr key={user.id}>
                            <td>{user.name}</td>
                            <td>{user.email}</td>
                            <td>{user.date}</td>
                            <td>
                              <span className={`subscription-badge ${user.subscription.toLowerCase()}`}>
                                {user.subscription}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  
                  <div className="admin-panel">
                    <div className="panel-header">
                      <h3>Recent Tools</h3>
                      <button className="view-all-button">View All</button>
                    </div>
                    
                    <table className="admin-table">
                      <thead>
                        <tr>
                          <th>Name</th>
                          <th>Category</th>
                          <th>Status</th>
                          <th>Rating</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recentTools.map(tool => (
                          <tr key={tool.id}>
                            <td>{tool.name}</td>
                            <td>{tool.category}</td>
                            <td>
                              <span className={`status-badge ${tool.status.toLowerCase()}`}>
                                {tool.status}
                              </span>
                            </td>
                            <td>{tool.rating}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'users' && (
              <div className="admin-users">
                <h2>User Management</h2>
                <p>Manage user accounts, subscriptions, and permissions.</p>
                
                {/* User management content would go here */}
                <div className="placeholder-content">
                  <p>User management interface is under development.</p>
                </div>
              </div>
            )}
            
            {activeTab === 'tools' && (
              <div className="admin-tools">
                <h2>AI Tools Management</h2>
                <p>Add, edit, and manage AI tools in the directory.</p>
                
                {/* Tools management content would go here */}
                <div className="placeholder-content">
                  <p>AI tools management interface is under development.</p>
                </div>
              </div>
            )}
            
            {activeTab === 'reviews' && (
              <div className="admin-reviews">
                <h2>Review Management</h2>
                <p>Moderate and manage user reviews.</p>
                
                {/* Reviews management content would go here */}
                <div className="placeholder-content">
                  <p>Review management interface is under development.</p>
                </div>
              </div>
            )}
            
            {activeTab === 'subscriptions' && (
              <div className="admin-subscriptions">
                <h2>Subscription Management</h2>
                <p>Manage subscription plans and user subscriptions.</p>
                
                {/* Subscription management content would go here */}
                <div className="placeholder-content">
                  <p>Subscription management interface is under development.</p>
                </div>
              </div>
            )}
            
            {activeTab === 'settings' && (
              <div className="admin-settings">
                <h2>System Settings</h2>
                <p>Configure system settings and preferences.</p>
                
                {/* Settings content would go here */}
                <div className="placeholder-content">
                  <p>Settings interface is under development.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;


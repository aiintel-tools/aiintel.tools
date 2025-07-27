import React, { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

const AuthPage = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [mode, setMode] = useState(
    new URLSearchParams(location.search).get('mode') || 'login'
  )
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    company: '',
    industry: '',
    agreeTerms: false
  })
  
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }
  
  const handleSubmit = (e) => {
    e.preventDefault()
    // In a real app, this would handle authentication
    console.log('Form submitted:', formData)
    navigate('/')
  }
  
  const toggleMode = () => {
    setMode(mode === 'login' ? 'register' : 'login')
  }

  return (
    <div className="auth-page">
      <div className="container">
        <div className="auth-card">
          <div className="auth-tabs">
            <button 
              className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
              onClick={() => setMode('login')}
            >
              Sign In
            </button>
            <button 
              className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
              onClick={() => setMode('register')}
            >
              Sign Up
            </button>
          </div>
          
          <div className="auth-content">
            <h1>{mode === 'login' ? 'Welcome Back' : 'Create Your Account'}</h1>
            <p>
              {mode === 'login' 
                ? 'Sign in to access your account and saved tools.' 
                : 'Join thousands of professionals discovering the best AI tools.'}
            </p>
            
            <form onSubmit={handleSubmit} className="auth-form">
              {mode === 'register' && (
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">First Name</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="lastName">Last Name</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>
              )}
              
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </div>
              
              {mode === 'register' && (
                <>
                  <div className="form-group">
                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <input
                      type="password"
                      id="confirmPassword"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  
                  <div className="form-section">
                    <h3>Professional Information (Optional)</h3>
                    
                    <div className="form-group">
                      <label htmlFor="company">Company</label>
                      <input
                        type="text"
                        id="company"
                        name="company"
                        value={formData.company}
                        onChange={handleChange}
                      />
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="industry">Industry</label>
                      <select
                        id="industry"
                        name="industry"
                        value={formData.industry}
                        onChange={handleChange}
                      >
                        <option value="">Select Industry</option>
                        <option value="technology">Technology</option>
                        <option value="healthcare">Healthcare</option>
                        <option value="finance">Finance</option>
                        <option value="education">Education</option>
                        <option value="marketing">Marketing</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                    
                    <div className="form-group checkbox">
                      <input
                        type="checkbox"
                        id="agreeTerms"
                        name="agreeTerms"
                        checked={formData.agreeTerms}
                        onChange={handleChange}
                        required
                      />
                      <label htmlFor="agreeTerms">
                        I agree to the <a href="/terms">Terms of Service</a> and <a href="/privacy">Privacy Policy</a>
                      </label>
                    </div>
                  </div>
                </>
              )}
              
              <button type="submit" className="auth-button">
                {mode === 'login' ? 'Sign In' : 'Create Account'}
              </button>
              
              {mode === 'login' && (
                <div className="auth-links">
                  <a href="/forgot-password">Forgot password?</a>
                  <button type="button" onClick={toggleMode} className="link-button">
                    Don't have an account? Sign up
                  </button>
                </div>
              )}
              
              {mode === 'register' && (
                <div className="auth-links">
                  <button type="button" onClick={toggleMode} className="link-button">
                    Already have an account? Sign in
                  </button>
                </div>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuthPage


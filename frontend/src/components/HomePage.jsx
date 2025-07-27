import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const HomePage = () => {
  // State for email capture
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  
  // Mock data
  const featuredTools = [
    {
      id: 1,
      name: 'ChatGPT',
      category: 'Conversational AI',
      description: 'Advanced AI chatbot for conversations and content creation',
      rating: 4.8,
      accessLevel: 'Public'
    },
    {
      id: 2,
      name: 'Midjourney',
      category: 'Image Generation',
      description: 'AI-powered image generation from text prompts',
      rating: 4.7,
      accessLevel: 'Premium'
    },
    {
      id: 3,
      name: 'GitHub Copilot',
      category: 'Code Assistant',
      description: 'AI pair programmer that helps you write code faster',
      rating: 4.6,
      accessLevel: 'Business'
    }
  ]
  
  const testimonials = [
    {
      id: 1,
      name: 'Sarah Johnson',
      role: 'Marketing Director',
      company: 'TechGrowth Inc.',
      image: 'https://randomuser.me/api/portraits/women/32.jpg',
      quote: 'This directory saved me countless hours of research. I found the perfect AI tools for our marketing campaigns and increased our ROI by 35%.'
    },
    {
      id: 2,
      name: 'Michael Chen',
      role: 'CTO',
      company: 'InnovateSoft',
      image: 'https://randomuser.me/api/portraits/men/45.jpg',
      quote: 'The premium membership pays for itself. Access to business-only tools and detailed guides helped us implement AI solutions in half the expected time.'
    },
    {
      id: 3,
      name: 'Jessica Williams',
      role: 'Small Business Owner',
      company: 'Creative Solutions',
      image: 'https://randomuser.me/api/portraits/women/68.jpg',
      quote: 'As a small business owner, I was overwhelmed by all the AI options. This directory helped me find affordable tools that work for my budget and needs.'
    }
  ]
  
  const membershipBenefits = [
    {
      title: 'Discover the Right Tools',
      description: 'Find AI tools perfectly matched to your industry, business size, and specific needs',
      icon: '🔍'
    },
    {
      title: 'Save Time & Money',
      description: 'Avoid costly trial-and-error with our verified reviews and detailed comparisons',
      icon: '💰'
    },
    {
      title: 'Implementation Guides',
      description: 'Step-by-step tutorials and best practices to maximize your ROI with each tool',
      icon: '📚'
    },
    {
      title: 'Stay Ahead of Competitors',
      description: 'Get early access to emerging AI tools and technologies before they go mainstream',
      icon: '🚀'
    }
  ]
  
  const handleEmailSubmit = (e) => {
    e.preventDefault();
    if (!email) return;
    
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setShowSuccessMessage(true);
      setEmail('');
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setShowSuccessMessage(false);
      }, 3000);
    }, 1000);
  };

  return (
    <div className="home-page">
      {/* Hero Section - Enhanced with stronger value proposition */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1>
              Find & Implement the <span className="highlight">Perfect AI Tools</span><br />
              to Grow Your Business
            </h1>
            <p className="hero-subtitle">
              Join 15,000+ business owners who use our directory to discover, compare, and implement 
              the best AI tools for their specific industry needs.
            </p>
            
            <div className="hero-cta">
              <Link to="/auth?mode=register" className="primary-button pulse-animation">
                Start Your Free Trial
              </Link>
              <Link to="/pricing" className="secondary-button">
                View Membership Options
              </Link>
            </div>
            
            <div className="trust-badges">
              <span>No credit card required</span>
              <span>•</span>
              <span>14-day free trial</span>
              <span>•</span>
              <span>Cancel anytime</span>
            </div>
          </div>
          
          <div className="hero-image">
            {/* Placeholder for hero image - could be a screenshot of the tool dashboard */}
            <div className="image-placeholder">
              <img src="https://via.placeholder.com/600x400" alt="AI Directory Dashboard" />
            </div>
          </div>
        </div>
      </section>
      
      {/* Social Proof Section */}
      <section className="social-proof">
        <div className="container">
          <div className="stats">
            <div className="stat">
              <h2>250+</h2>
              <p>AI Tools Listed</p>
            </div>
            <div className="stat">
              <h2>15,000+</h2>
              <p>Active Users</p>
            </div>
            <div className="stat">
              <h2>8,500+</h2>
              <p>Verified Reviews</p>
            </div>
          </div>
          
          <div className="trusted-by">
            <p>Trusted by innovative companies:</p>
            <div className="company-logos">
              <span>Microsoft</span>
              <span>Adobe</span>
              <span>Shopify</span>
              <span>Salesforce</span>
              <span>HubSpot</span>
            </div>
          </div>
        </div>
      </section>
      
      {/* Value Proposition Section */}
      <section className="value-proposition">
        <div className="container">
          <h2 className="section-title">Why Business Owners Choose Our Directory</h2>
          
          <div className="benefits-grid">
            {membershipBenefits.map((benefit, index) => (
              <div key={index} className="benefit-card">
                <div className="benefit-icon">{benefit.icon}</div>
                <h3>{benefit.title}</h3>
                <p>{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Featured Tools Section - Enhanced with access level badges */}
      <section className="featured-tools">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Featured AI Tools</h2>
            <Link to="/tools" className="view-all">View All Tools →</Link>
          </div>
          
          <div className="tools-grid">
            {featuredTools.map(tool => (
              <div key={tool.id} className="tool-card">
                <div className="tool-header">
                  <div className="tool-category">{tool.category}</div>
                  <div className={`access-badge ${tool.accessLevel.toLowerCase()}`}>
                    {tool.accessLevel}
                  </div>
                </div>
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
          
          <div className="tools-cta">
            <p>Unlock access to 200+ more AI tools with detailed implementation guides</p>
            <Link to="/pricing" className="secondary-button">
              Compare Membership Options
            </Link>
          </div>
        </div>
      </section>
      
      {/* Testimonials Section */}
      <section className="testimonials">
        <div className="container">
          <h2 className="section-title">What Our Members Say</h2>
          
          <div className="testimonials-grid">
            {testimonials.map(testimonial => (
              <div key={testimonial.id} className="testimonial-card">
                <div className="quote">"</div>
                <p className="testimonial-text">{testimonial.quote}</p>
                <div className="testimonial-author">
                  <img src={testimonial.image} alt={testimonial.name} className="author-image" />
                  <div className="author-info">
                    <h4>{testimonial.name}</h4>
                    <p>{testimonial.role}, {testimonial.company}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* How It Works Section */}
      <section className="how-it-works">
        <div className="container">
          <h2 className="section-title">How Our Directory Helps You Succeed</h2>
          
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Discover</h3>
              <p>Browse our curated directory of 250+ AI tools organized by industry, function, and business size</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Compare</h3>
              <p>Read verified reviews, compare features, and find the perfect tools for your specific needs</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Implement</h3>
              <p>Follow our detailed guides to quickly implement and start seeing ROI from your chosen tools</p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Email Capture Section */}
      <section className="email-capture">
        <div className="container">
          <h2>Get Weekly AI Tool Recommendations</h2>
          <p>Join 25,000+ subscribers who receive our curated list of the best new AI tools for business</p>
          
          <form onSubmit={handleEmailSubmit} className="email-form">
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email address" 
              required
            />
            <button 
              type="submit" 
              disabled={isSubmitting}
              className="primary-button"
            >
              {isSubmitting ? 'Subscribing...' : 'Subscribe'}
            </button>
          </form>
          
          {showSuccessMessage && (
            <div className="success-message">
              Thank you for subscribing! Check your inbox for a confirmation email.
            </div>
          )}
          
          <div className="privacy-note">
            We respect your privacy. Unsubscribe at any time.
          </div>
        </div>
      </section>
      
      {/* Membership CTA Section - Enhanced with urgency and FOMO */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Transform Your Business with AI?</h2>
            <p>Join thousands of business owners who are gaining a competitive edge with our premium AI tool directory.</p>
            
            <div className="cta-features">
              <div className="feature">✓ Unlimited access to 250+ AI tools</div>
              <div className="feature">✓ Exclusive implementation guides</div>
              <div className="feature">✓ Premium-only tools and reviews</div>
              <div className="feature">✓ Early access to new AI technologies</div>
            </div>
            
            <div className="cta-buttons">
              <Link to="/auth?mode=register" className="primary-button pulse-animation">
                Start Your Free Trial
              </Link>
              <Link to="/pricing" className="text-link">
                View pricing options →
              </Link>
            </div>
            
            <div className="limited-offer">
              <span className="offer-tag">Limited Time Offer</span>
              <span>Get 20% off annual plans this week only!</span>
            </div>
          </div>
        </div>
      </section>
      
      {/* FAQ Section */}
      <section className="faq-section">
        <div className="container">
          <h2 className="section-title">Frequently Asked Questions</h2>
          
          <div className="faq-grid">
            <div className="faq-item">
              <h3>What makes this directory different from others?</h3>
              <p>Unlike other directories, we focus on business implementation with detailed guides, ROI calculators, and industry-specific recommendations tailored to your business needs.</p>
            </div>
            <div className="faq-item">
              <h3>How often are new tools added?</h3>
              <p>We add 10-15 new tools every week after thorough vetting and testing by our team of AI experts and business consultants.</p>
            </div>
            <div className="faq-item">
              <h3>Can I cancel my membership anytime?</h3>
              <p>Yes, you can cancel your membership at any time with no questions asked. We offer a 14-day money-back guarantee if you're not satisfied.</p>
            </div>
            <div className="faq-item">
              <h3>Do you offer team or enterprise plans?</h3>
              <p>Yes, we offer special plans for teams and enterprises with additional features like API access and custom integrations. Contact us for details.</p>
            </div>
          </div>
          
          <div className="more-questions">
            <p>Have more questions? <Link to="/contact">Contact our support team</Link></p>
          </div>
        </div>
      </section>
      
      {/* Final CTA Section */}
      <section className="final-cta">
        <div className="container">
          <h2>Join 15,000+ Business Owners Already Using Our Directory</h2>
          <p>Start your free 14-day trial today. No credit card required.</p>
          <Link to="/auth?mode=register" className="primary-button large pulse-animation">
            Get Started Now
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage


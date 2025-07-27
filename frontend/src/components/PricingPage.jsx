import React from 'react'
import { Link } from 'react-router-dom'

const PricingPage = () => {
  const plans = [
    {
      name: 'Free',
      price: '$0',
      description: 'Perfect for getting started',
      features: [
        'Browse all AI tools',
        'Basic search and filters',
        'Tool ratings and reviews',
        'Community support'
      ],
      popular: false
    },
    {
      name: 'Premium',
      price: '$9',
      description: 'Best for professionals',
      features: [
        'Everything in Free',
        'Advanced search filters',
        'Save favorite tools',
        'Write reviews',
        'Priority support',
        'Export tool lists'
      ],
      popular: true
    },
    {
      name: 'Business',
      price: '$29',
      description: 'For teams and organizations',
      features: [
        'Everything in Premium',
        'Team collaboration',
        'Custom categories',
        'API access',
        'Analytics dashboard',
        'Dedicated support'
      ],
      popular: false
    }
  ]

  return (
    <div className="pricing-page">
      <div className="container">
        <div className="page-header">
          <h1>Choose Your Plan</h1>
          <p>Get access to premium features and unlock the full potential of our AI tools directory.</p>
        </div>
        
        <div className="pricing-plans">
          {plans.map((plan) => (
            <div 
              key={plan.name} 
              className={`pricing-card ${plan.popular ? 'popular' : ''}`}
            >
              {plan.popular && (
                <div className="popular-badge">Most Popular</div>
              )}
              
              <div className="plan-header">
                <h2>{plan.name}</h2>
                <div className="plan-price">
                  {plan.price}<span>/month</span>
                </div>
                <p>{plan.description}</p>
              </div>
              
              <div className="plan-features">
                <ul>
                  {plan.features.map((feature, index) => (
                    <li key={index}>
                      <span className="check-icon">✓</span> {feature}
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="plan-action">
                <Link 
                  to="/auth?mode=register" 
                  className={`plan-button ${plan.popular ? 'primary' : 'secondary'}`}
                >
                  {plan.name === 'Free' ? 'Get Started' : 'Choose Plan'}
                </Link>
              </div>
            </div>
          ))}
        </div>
        
        <div className="pricing-info">
          <p>All plans include a 14-day free trial. No credit card required.</p>
          <p>Need a custom solution? <Link to="/contact">Contact us</Link></p>
        </div>
      </div>
    </div>
  )
}

export default PricingPage


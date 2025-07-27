import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const navigate = useNavigate()

  return (
    <header className="header">
      <div className="container">
        <div className="logo">
          <Link to="/">AI Directory</Link>
        </div>
        
        <nav className={`nav ${isMenuOpen ? 'active' : ''}`}>
          <ul className="nav-list">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/tools">Browse Tools</Link></li>
            <li><Link to="/pricing">Pricing</Link></li>
          </ul>
        </nav>
        
        <div className="auth-buttons">
          <button onClick={() => navigate('/auth')}>Sign In</button>
          <button onClick={() => navigate('/auth?mode=register')} className="btn-primary">
            Get Started
          </button>
        </div>
        
        <button 
          className="menu-toggle"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          Menu
        </button>
      </div>
    </header>
  )
}

export default Header


import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Header from './components/Header'
import HomePage from './components/HomePage'
import ToolsPage from './components/ToolsPage'
import PricingPage from './components/PricingPage'
import AuthPage from './components/AuthPage'
import AdminLogin from './components/AdminLogin'
import Footer from './components/Footer'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="*" element={
            <>
              <Header />
              <main>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/tools" element={<ToolsPage />} />
                  <Route path="/pricing" element={<PricingPage />} />
                  <Route path="/auth" element={<AuthPage />} />
                </Routes>
              </main>
              <Footer />
            </>
          } />
        </Routes>
      </div>
    </Router>
  )
}

export default App


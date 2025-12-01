import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useState, useEffect, useRef } from 'react'

function Layout({ children }) {
  const location = useLocation()
  const isLoginPage = location.pathname === "/"
  const { logout } = useAuth()
  const [showCreateDropdown, setShowCreateDropdown] = useState(false)
  const dropdownRef = useRef(null)


  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowCreateDropdown(false)
      }
    }

    if (showCreateDropdown) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showCreateDropdown])

  return (
    <>
      {!isLoginPage && (
        <header id="main-navigation">
          <h1>
            <Link to="/dashboard">Expense Tracker</Link>
          </h1>
          <nav>
            <div className="dropdown-container" ref={dropdownRef}>
              <Link
                to="#"
                onClick={(e) => {
                  e.preventDefault()
                  setShowCreateDropdown(!showCreateDropdown)
                }}
              >
                Create
              </Link>
              {showCreateDropdown && (
                <div className="dropdown-menu">
                  <Link
                    to="/create-expense"
                    onClick={() => setShowCreateDropdown(false)}
                  >
                    Expense
                  </Link>
                  <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
                  <Link to="/create-income" onClick={() => setShowCreateDropdown(false)}>Income</Link>
                  <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
                  <Link to="/create-budget" onClick={() => setShowCreateDropdown(false)}>Budget</Link>
                  <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
                  <Link to="/create-goal" onClick={() => setShowCreateDropdown(false)}>Goal</Link>
                </div>
              )}
            </div>
            <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
            <Link to="/expenses">Expenses</Link>
            <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
            <Link to="/income">Income</Link>
            <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
            <Link to="/budgets">Budgets</Link>
            <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
            <Link to="/goals">Goals</Link>
            <span style={{ marginLeft: '5px', marginRight: '5px' }}></span>
            <Link onClick={() => logout()}>Logout</Link>
          </nav>
        </header>
      )}
      <main className="page-content">
        {children}
      </main>
    </>
  )
}

export default Layout


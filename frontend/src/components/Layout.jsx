import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

function Layout({ children }) {
  const location = useLocation()
  const isLoginPage = location.pathname === "/"
  const { logout } = useAuth()


  return (
    <>
      {!isLoginPage && (
        <header id="main-navigation">
          <h1>
            <Link to="/dashboard">Expense Tracker</Link>
          </h1>
          <nav>
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


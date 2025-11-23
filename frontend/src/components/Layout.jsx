import { Link } from 'react-router-dom'

function Layout({ children }) {
  return (
    <>
      <header id="main-navigation">
        <h1>
          <Link to="/">Expense Tracker</Link>
        </h1>
        <nav>
          <Link to="/expenses">Expenses</Link>
          <Link to="/income">Income</Link>
          <Link to="/budgets">Budgets</Link>
          <Link to="/goals">Goals</Link>
        </nav>
      </header>
      <main className="page-content">
        {children}
      </main>
    </>
  )
}

export default Layout


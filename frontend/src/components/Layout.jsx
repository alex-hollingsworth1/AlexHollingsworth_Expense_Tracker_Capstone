import { Link } from 'react-router-dom'

function Layout({ children }) {
  return (
    <>
      <header id="main-navigation">
        <h1>
          <Link to="/">Expense Tracker</Link>
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
        </nav>
      </header>
      <main className="page-content">
        {children}
      </main>
    </>
  )
}

export default Layout


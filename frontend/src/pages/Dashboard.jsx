import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchDashboardData } from '../services/api'
import '../Dashboard.css'

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null)

  useEffect(() => {
    fetchDashboardData()
      .then(setDashboardData)
      .catch(console.error)
  }, [])

  return (
    <div>
      <h1>Dashboard</h1>

      {/* Summary Section */}
      <div className="dashboard-summary">
        <div className="summary-pill-income">
          Total Income<br />
          <strong>${dashboardData?.income_total?.toFixed(2) || '0.00'}</strong>
        </div>
        <div className="summary-pill-expense">
          Total Expenses<br />
          <strong>${dashboardData?.expense_total?.toFixed(2) || '0.00'}</strong>
        </div>
        <div className="summary-pill-budget">
          Budgets<br />
          <strong>{dashboardData?.number_of_budgets || 0}</strong>
        </div>
        <div className="summary-pill-goal">
          Goals<br />
          <strong>{dashboardData?.number_of_goals || 0}</strong>
        </div>
      </div>

      {/* Dashboard Cards Section */}
      <div className="dashboard-layout">

      <section className="dashboard-card dashboard-card-income">
          <h2>Recent Income</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_income?.length > 0 ? (
              dashboardData.recent_income.map((income) => (
                <li key={income.id}>
                  <Link to={`/income/${income.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <article className="income-item">
                      <h3>{income.category.name}</h3>
                      <p className="meta">
                        <strong>Date:</strong> {income.date} · <strong>Amount:</strong> ${income.amount}
                      </p>
                      <p>{income.note || 'No note provided.'}</p>
                    </article>
                  </Link>
                </li>
              ))
            ) : (
              <li>No income entries yet.</li>
            )}
          </ul>
        </section>
        
        <section className="dashboard-card dashboard-card-expense">
          <h2>Recent Expenses</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_expenses?.length > 0 ? (
              dashboardData.recent_expenses.map((expense) => (
                <li key={expense.id}>
                  <Link to={`/expenses/${expense.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <article className="expense-item">
                      <h3>{expense.category.name}</h3>
                      <p className="meta">
                        <strong>Date:</strong> {expense.date} · <strong>Amount:</strong> ${expense.amount}
                      </p>
                      <p>{expense.note || 'No note provided.'}</p>
                    </article>
                  </Link>
                </li>
              ))
            ) : (
              <li>No expenses yet.</li>
            )}
          </ul>
        </section>



        <section className="dashboard-card dashboard-card-budget">
          <h2>Budgets</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_budgets?.length > 0 ? (
              dashboardData.recent_budgets.map((budget) => (
                <li key={budget.id}>
                  <Link to={`/budgets/${budget.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <article className="budget-item">
                      <h3>{budget.category.name}</h3>
                      <p className="meta">
                        <strong>Amount:</strong> ${budget.amount} · <strong>Period:</strong> {budget.start_date} to {budget.end_date}
                      </p>
                    </article>
                  </Link>
                </li>
              ))
            ) : (
              <li>No budgets configured yet.</li>
            )}
          </ul>
        </section>

        <section className="dashboard-card dashboard-card-goal">
          <h2>Goals</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_goals?.length > 0 ? (
              dashboardData.recent_goals.map((goal) => (
                <li key={goal.id}>
                  <Link to={`/goals/${goal.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <article className="goal-item">
                      <h3>{goal.name}</h3>
                      <p className="meta">
                        <strong>Target:</strong> ${goal.target} · <strong>Deadline:</strong> {goal.deadline} ·
                      </p>
                      <p><strong>Status:</strong> {goal.status}</p>
                    </article>
                  </Link>

                </li>
              ))
            ) : (
              <li>No goals defined yet.</li>
            )}
          </ul>
        </section>
      </div>
    </div>
  )
}

export default Dashboard


import { useEffect, useState } from 'react'
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
        <div className="summary-pill">
          Total Income<br />
          <strong>${dashboardData?.income_total?.toFixed(2) || '0.00'}</strong>
        </div>
        <div className="summary-pill">
          Total Expenses<br />
          <strong>${dashboardData?.expense_total?.toFixed(2) || '0.00'}</strong>
        </div>
        <div className={`summary-pill ${(dashboardData?.net_total || 0) >= 0 ? 'net-positive' : 'net-negative'}`}>
          Budgets<br />
          <strong>{dashboardData?.number_of_budgets || 0}</strong>
        </div>
        <div className={`summary-pill ${(dashboardData?.net_total || 0) >= 0 ? 'net-positive' : 'net-negative'}`}>
          Goals<br />
          <strong>{dashboardData?.number_of_goals || 0}</strong>
        </div>
      </div>

      {/* Dashboard Cards Section */}
      <div className="dashboard-layout">
        <section className="dashboard-card">
          <h2>Recent Expenses</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_expenses?.length > 0 ? (
              dashboardData.recent_expenses.map((expense) => (
                <li key={expense.id}>
                  <article>
                    <h3>{expense.category.name}</h3>
                    <p className="meta">
                      <strong>Date:</strong> {expense.date} · <strong>Amount:</strong> ${expense.amount}
                    </p>
                    <p>{expense.note || 'No note provided.'}</p>
                  </article>
                </li>
              ))
            ) : (
              <li>No expenses yet.</li>
            )}
          </ul>
        </section>

        <section className="dashboard-card">
          <h2>Recent Income</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_income?.length > 0 ? (
              dashboardData.recent_income.map((income) => (
                <li key={income.id}>
                  <article>
                    <h3>{income.category.name}</h3>
                    <p className="meta">
                      <strong>Date:</strong> {income.date} · <strong>Amount:</strong> ${income.amount}
                    </p>
                    <p>{income.note || 'No note provided.'}</p>
                  </article>
                </li>
              ))
            ) : (
              <li>No income entries yet.</li>
            )}
          </ul>
        </section>

        <section className="dashboard-card">
          <h2>Budgets</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_budgets?.length > 0 ? (
              dashboardData.recent_budgets.map((budget) => (
                <li key={budget.id}>
                  <article>
                    <h3>{budget.category.name}</h3>
                    <p className="meta">
                      <strong>Amount:</strong> ${budget.amount} · <strong>Period:</strong> {budget.start_date} to {budget.end_date}
                    </p>
                  </article>
                </li>
              ))
            ) : (
              <li>No budgets configured yet.</li>
            )}
          </ul>
        </section>

        <section className="dashboard-card">
          <h2>Goals</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {dashboardData?.recent_goals?.length > 0 ? (
              dashboardData.recent_goals.map((goal) => (
                <li key={goal.id}>
                  <article>
                    <h3>{goal.name}</h3>
                    <p className="meta">
                      <strong>Target:</strong> ${goal.target} · <strong>Deadline:</strong> {goal.deadline} · 
                    </p>
                    <p><strong>Status:</strong> {goal.status}</p>
                  </article>
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


import { useEffect, useState } from 'react'
import { fetchDashboardData } from '../services/api'

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
      <p>Welcome to your Expense Tracker Dashboard</p>
      <ul>
        {dashboardData?.recent_expenses.map((expense) => (
          <li key={expense.id}>
            <span>{expense.category.name}</span>
            <span>{expense.amount}</span>
            <span>{expense.date}</span>
            <span>{expense.note}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Dashboard


import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchBudgets } from '../services/api'
import '../Transactions.css'

function BudgetList() {
  const [budgets, setBudgets] = useState([])

  useEffect(() => {
    fetchBudgets()
    .then(setBudgets)
    .catch(console.error)
  }, [])

  return (
    <section className="section-listing">
      <h1>Budgets</h1>
      {budgets.length > 0 ? (
        <ul>
          {budgets.map((budget) => (
            <li key={budget.id}>
              <Link to={`/budgets/${budget.id}`}>
              <article>
                <h2>{budget.category.name}</h2>
                <p className="meta">
                  <strong>Amount:</strong> ${budget.amount} · <strong>Period:</strong> {budget.start_date} to {budget.end_date}
                </p>
                <p>{budget.note || 'No note provided.'}</p>
              </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No budgets yet.</p>
      )}
    </section>
  )
}

export default BudgetList


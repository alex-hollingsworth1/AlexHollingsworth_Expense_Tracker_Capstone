import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchExpenses } from '../services/api'
import '../Transactions.css'

function ExpenseList() {

  const [expenses, setExpenses] = useState([])

  useEffect(() => {
    fetchExpenses()
    .then(setExpenses)
    .catch(console.error)
  }, [])

  return (
    <section className="section-listing">
      <h1>Expenses</h1>
      {expenses.length > 0 ? (
        <ul>
          {expenses.map((expense) => (
            <li key={expense.id}>
              <Link to={`/expenses/${expense.id}`}>
                <article>
                  <h2>{expense.category.name}</h2>
                  <p className="meta">
                    <strong>Date:</strong> {expense.date} · <strong>Amount:</strong> ${expense.amount}
                  </p>
                  <p>{expense.note || 'No note provided.'}</p>
                </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No expenses yet.</p>
      )}
    </section>
  )
}

export default ExpenseList


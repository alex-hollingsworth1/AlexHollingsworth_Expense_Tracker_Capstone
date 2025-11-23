import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchIncomes } from '../services/api'
import '../Transactions.css'

function IncomeList() {
  const [incomes, setIncomes] = useState([])

  useEffect(() => {
    fetchIncomes()
    .then(setIncomes)
    .catch(console.error)
  }, [])

  return (
    <section className="section-listing">
      <h1>Income</h1>
      {incomes.length > 0 ? (
        <ul>
          {incomes.map((income) => (
            <li key={income.id}>
              <Link to={`/income/${income.id}`}>
                <article>
                  <h2>{income.category.name}</h2>
                  <p className="meta">
                    <strong>Date:</strong> {income.date} · <strong>Amount:</strong> ${income.amount}
                  </p>
                  <p>{income.note || 'No note provided.'}</p>
                </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No income yet.</p>
      )}  
    </section>
  )
}

export default IncomeList


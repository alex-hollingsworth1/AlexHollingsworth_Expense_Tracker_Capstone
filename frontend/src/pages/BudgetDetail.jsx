import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchBudget } from '../services/api'
import '../Transactions.css'

// ExpenseDetail.jsx

const BudgetDetail = () => {
    const { id } = useParams()
    const [budget, setBudget] = useState(null)
    
    useEffect(() => {
    fetchBudget(id)
    .then(setBudget)
    .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <h1>Budget Detail</h1>
            {budget ? (
                <article>
                    <h2>{budget.category.name}</h2>
                    <p className="meta">
                        <strong>Amount:</strong> ${budget.amount} · <strong>Period:</strong> {budget.start_date} to {budget.end_date}
                    </p>
                    <p>{budget.note || 'No note provided.'}</p>
                </article>
            ) : (
                <p>No budget found.</p>
            )}
        </section>
    )
}

export default BudgetDetail

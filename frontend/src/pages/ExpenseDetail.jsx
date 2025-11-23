import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchExpense } from '../services/api'
import '../Transactions.css'

// ExpenseDetail.jsx

const ExpenseDetail = () => {
    const { id } = useParams()
    const [expense, setExpense] = useState(null)
    
    useEffect(() => {
    fetchExpense(id)
    .then(setExpense)
    .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <h1>Expense Detail</h1>
            {expense ? (
                <article>
                    <h2>{expense.category.name}</h2>
                    <p className="meta">
                        <strong>Amount:</strong> ${expense.amount} · <strong>Date:</strong> {expense.date}
                    </p>
                    <p>{expense.note || 'No note provided.'}</p>
                </article>
            ) : (
                <p>No expense found.</p>
            )}
        </section>
    )
}

export default ExpenseDetail

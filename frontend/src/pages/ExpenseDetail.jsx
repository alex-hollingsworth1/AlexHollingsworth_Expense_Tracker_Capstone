import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchExpense } from '../services/api'
import '../styles/Transactions.css'

const ExpenseDetail = () => {
    const { id } = useParams()
    const [expense, setExpense] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchExpense(id)
            .then(setExpense)
            .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <div style={{ textAlign: 'left', marginBottom: '1rem', marginLeft: '-1rem' }}>
                <Link 
                    to="/expenses" 
                    className="summary-pill summary-pill-small"
                >
                    ← Back to Expenses
                </Link>
            </div>
            <h1>Expense Detail</h1>
            {expense ? (
                <div className="detail-card detail-card-expense">
                    <article>
                        <h2>{expense.category.name}</h2>
                        <p className="meta">
                            <strong>Amount:</strong> ${expense.amount}
                        </p>
                        <p>
                            <strong>Date:</strong> {expense.date}
                        </p>
                        <p>
                            <strong>Client:</strong> {expense.client?.name || 'No client provided.'}
                        </p>
                        <p>
                            <strong>Project:</strong> {expense.project?.name || 'No project provided.'}
                        </p>
                        <p>
                            <strong>Note:</strong> {expense.note || 'No note provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-expense">
                    <p>Loading expense details...</p>
                </div>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-expense/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill-small-delete-red" onClick={() => navigate(`/delete-expense/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default ExpenseDetail

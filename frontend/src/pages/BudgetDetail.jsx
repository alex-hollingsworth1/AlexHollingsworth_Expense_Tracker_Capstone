import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchBudget } from '../services/api'
import '../styles/Transactions.css'

const BudgetDetail = () => {
    const { id } = useParams()
    const [budget, setBudget] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchBudget(id)
            .then(setBudget)
            .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <div style={{ textAlign: 'left', marginBottom: '1rem', marginLeft: '-1rem' }}>
                <Link 
                    to="/budgets" 
                    className="summary-pill summary-pill-small"
                >
                    ← Back to Budgets
                </Link>
            </div>
            <h1>Budget Detail</h1>
            {budget ? (
                <div className="detail-card detail-card-budget">
                    <article>
                        <h2>{budget.category.name}</h2>
                        <p className="meta">
                            <strong>Amount:</strong> ${budget.amount}
                        </p>
                        <p>
                            <strong>Start Date:</strong> {budget.start_date}
                        </p>
                        <p>
                            <strong>End Date:</strong> {budget.end_date}
                        </p>
                        <p>
                            <strong>Note:</strong> {budget.note || 'No note provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-budget">
                    <p>Loading budget details...</p>
                </div>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-budget/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill-small-delete-red" onClick={() => navigate(`/delete-budget/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default BudgetDetail

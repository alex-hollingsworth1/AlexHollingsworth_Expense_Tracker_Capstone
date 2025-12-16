import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchIncome } from '../services/api'
import '../styles/Transactions.css'

const IncomeDetail = () => {
    const { id } = useParams()
    const [income, setIncome] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchIncome(id)
            .then(setIncome)
            .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <div style={{ textAlign: 'left', marginBottom: '1rem', marginLeft: '-1rem' }}>
                <Link 
                    to="/income" 
                    className="summary-pill summary-pill-small"
                >
                    ← Back to Income
                </Link>
            </div>
            <h1>Income Detail</h1>
            {income ? (
                <div className="detail-card detail-card-income">
                    <article>
                        <h2>{income.category.name}</h2>
                        <p className="meta">
                            <strong>Amount:</strong> ${income.amount}
                        </p>
                        <p>
                            <strong>Date:</strong> {income.date}
                        </p>
                        <p>
                            <strong>Client:</strong> {income.client?.name || 'No client provided.'}
                        </p>
                        <p>
                            <strong>Project:</strong> {income.project?.name || 'No project provided.'}
                        </p>
                        <p>
                            <strong>Note:</strong> {income.note || 'No note provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-income">
                    <p>Loading income details...</p>
                </div>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-income/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill-small-delete-red" onClick={() => navigate(`/delete-income/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default IncomeDetail

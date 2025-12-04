import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchIncome } from '../services/api'
import '../Transactions.css'

// ExpenseDetail.jsx

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
            <h1>Income Detail</h1>
            {income ? (
                <article>
                    <h2>{income.category.name}</h2>
                    <p className="meta">
                        <strong>Amount:</strong> ${income.amount} · <strong>Date:</strong> {income.date}
                    </p>
                    <p>{income.note || 'No note provided.'}</p>
                </article>
            ) : (
                <p>No income found.</p>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-income/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/delete-income/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default IncomeDetail

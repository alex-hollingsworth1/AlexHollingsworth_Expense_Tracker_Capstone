import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchIncome } from '../services/api'
import '../Transactions.css'

// ExpenseDetail.jsx

const IncomeDetail = () => {
    const { id } = useParams()
    const [income, setIncome] = useState(null)
    
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
        </section>
    )
}

export default IncomeDetail

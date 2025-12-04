import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchGoal } from '../services/api'
import '../Transactions.css'

// ExpenseDetail.jsx

const GoalDetail = () => {
    const { id } = useParams()
    const [goal, setGoal] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchGoal(id)
            .then(setGoal)
            .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <h1>Goal Detail</h1>
            {goal ? (
                <article>
                    <h2>{goal.name}</h2>
                    <p className="meta">
                        <strong>Target:</strong> ${goal.target} · <strong>Deadline:</strong> {goal.deadline}
                    </p>
                    <p>Status: {goal.status || 'No status provided.'}</p>
                </article>
            ) : (
                <p>No goal found.</p>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-goal/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/delete-goal/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default GoalDetail

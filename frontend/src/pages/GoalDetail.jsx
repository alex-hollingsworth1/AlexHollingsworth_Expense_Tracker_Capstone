import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchGoal } from '../services/api'
import '../Transactions.css'

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
            <div style={{ textAlign: 'left', marginBottom: '1rem', marginLeft: '-1rem' }}>
                <Link 
                    to="/goals" 
                    className="summary-pill summary-pill-small"
                >
                    ← Back to Goals
                </Link>
            </div>
            <h1>Goal Detail</h1>
            {goal ? (
                <div className="detail-card detail-card-goal">
                    <article>
                        <h2>{goal.name}</h2>
                        <p className="meta">
                            <strong>Target:</strong> ${goal.target}
                        </p>
                        <p>
                            <strong>Deadline:</strong> {goal.deadline}
                        </p>
                        <p>
                            <strong>Status:</strong> {goal.status || 'No status provided.'}
                        </p>
                        <p>
                            <strong>Note:</strong> {goal.note || 'No note provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-goal">
                    <p>Loading goal details...</p>
                </div>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-goal/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill-small-delete-red" onClick={() => navigate(`/delete-goal/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default GoalDetail

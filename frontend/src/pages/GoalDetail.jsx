import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchGoal } from '../services/api'
import '../Transactions.css'

// ExpenseDetail.jsx

const GoalDetail = () => {
    const { id } = useParams()
    const [goal, setGoal] = useState(null)
    
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
        </section>
    )
}

export default GoalDetail

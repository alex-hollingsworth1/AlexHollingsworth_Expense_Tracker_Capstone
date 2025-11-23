import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchGoals } from '../services/api'
import '../Transactions.css'

function GoalList() {
  const [goals, setGoals] = useState([])

  useEffect(() => {
    fetchGoals()
    .then(setGoals)
    .catch(console.error)
  }, [])

  return (
    <section className="section-listing">
      <h1>Goals</h1>
      {goals.length > 0 ? (
        <ul>
          {goals.map((goal) => (
            <li key={goal.id}>
              <Link to={`/goals/${goal.id}`}>
              <article>
                <h2>{goal.name}</h2>
                <p className="meta">
                  <strong>Target:</strong> ${goal.target} · <strong>Deadline:</strong> {goal.deadline} · <strong>Status:</strong> {goal.status}
                </p>
              </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No goals yet.</p>
      )}
    </section>
  )
}

export default GoalList


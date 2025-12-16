import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { deleteGoal, fetchGoal } from "../services/api";
import '../styles/Transactions.css'

function DeleteGoal() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [goal, setGoal] = useState(null)
    const [loading, setLoading] = useState(true)
    const [deleting, setDeleting] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)
    const [successMessage, setSuccessMessage] = useState(null)

    // Fetch the goal data
    useEffect(() => {
        fetchGoal(id)
            .then((goal) => {
                setGoal(goal)
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch goal details: ", error)
                setErrorMessage("Failed to fetch goal details")
                setLoading(false)
            })
    }, [id])

    const handleGoal = async (e) => {
        e.preventDefault()
        setErrorMessage(null)
        setDeleting(true)

        try {
            await deleteGoal(id)
            setSuccessMessage("Goal deleted successfully!")
            setTimeout(() => {
                navigate("/goals")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to delete goal. Please try again.")
            console.error(error)
            setDeleting(false)
        }
    }

    const handleCancel = () => {
        navigate(`/goals/${id}`)
    }

    if (loading) {
        return (
            <section className="section-detail">
                <div className="detail-card detail-card-goal">
                    <p>Loading goal...</p>
                </div>
            </section>
        )
    }

    return (
        <section className="section-detail">
            <h1>Delete Goal</h1>

            {/* Confirmation Warning Message */}
            <div className="error-message" style={{
                backgroundColor: '#fff3cd',
                borderColor: '#ffc107',
                color: '#856404',
                marginBottom: '20px'
            }}>
                <strong>Warning:</strong> Are you sure you want to delete this goal? This action cannot be undone.
            </div>

            {successMessage && (
                <div className="success-message">
                    {successMessage}
                </div>
            )}
            {errorMessage && (
                <div className="error-message">
                    {errorMessage}
                </div>
            )}

            {/* Display goal details (read-only) */}
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
                    <p>No goal found.</p>
                </div>
            )}

            {/* Action buttons */}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small-delete" onClick={handleCancel} disabled={deleting}>
                    Cancel
                </div>

                <div className="summary-pill summary-pill-small-delete" onClick={handleGoal} disabled={deleting}>
                    {deleting ? 'Deleting...' : 'Confirm Delete'}
                </div>
            </div>
        </section >
    )
}

export default DeleteGoal;
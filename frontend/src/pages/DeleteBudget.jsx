import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { deleteBudget, fetchBudget } from "../services/api";
import '../styles/Transactions.css'

function DeleteBudget() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [budget, setBudget] = useState(null)
    const [loading, setLoading] = useState(true)
    const [deleting, setDeleting] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)
    const [successMessage, setSuccessMessage] = useState(null)

    // Fetch the budget data
    useEffect(() => {
        fetchBudget(id)
            .then((budget) => {
                setBudget(budget)
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch budget details: ", error)
                setErrorMessage("Failed to fetch budget details")
                setLoading(false)
            })
    }, [id])

    const handleBudget = async (e) => {
        e.preventDefault()
        setErrorMessage(null)
        setDeleting(true)

        try {
            await deleteBudget(id)
            setSuccessMessage("Budget deleted successfully!")
            setTimeout(() => {
                navigate("/budgets")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to delete budget. Please try again.")
            console.error(error)
            setDeleting(false)
        }
    }

    const handleCancel = () => {
        navigate(`/budgets/${id}`)
    }

    if (loading) {
        return (
            <section className="section-detail">
                <div className="detail-card detail-card-budget">
                    <p>Loading budget...</p>
                </div>
            </section>
        )
    }

    return (
        <section className="section-detail">
            <h1>Delete Budget</h1>

            {/* Confirmation Warning Message */}
            <div className="error-message" style={{
                backgroundColor: '#fff3cd',
                borderColor: '#ffc107',
                color: '#856404',
                marginBottom: '20px'
            }}>
                <strong>Warning:</strong> Are you sure you want to delete this budget? This action cannot be undone.
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

            {/* Display budget details (read-only) */}
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
                    <p>No budget found.</p>
                </div>
            )}

            {/* Action buttons */}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small-delete" onClick={handleCancel} disabled={deleting}>
                    Cancel
                </div>

                <div className="summary-pill summary-pill-small-delete" onClick={handleBudget} disabled={deleting}>
                    {deleting ? 'Deleting...' : 'Confirm Delete'}
                </div>
            </div>
        </section >
    )
}

export default DeleteBudget;
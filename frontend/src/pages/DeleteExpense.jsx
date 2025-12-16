import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchExpense, deleteExpense } from "../services/api";
import '../styles/Transactions.css'

function DeleteExpense() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [expense, setExpense] = useState(null)
    const [loading, setLoading] = useState(true)
    const [deleting, setDeleting] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)
    const [successMessage, setSuccessMessage] = useState(null)

    // Fetch the expense data
    useEffect(() => {
        fetchExpense(id)
            .then((expense) => {
                setExpense(expense)
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch expense: ", error)
                setErrorMessage("Failed to load expense")
                setLoading(false)
            })
    }, [id])

    const handleDelete = async (e) => {
        e.preventDefault()
        setErrorMessage(null)
        setDeleting(true)

        try {
            await deleteExpense(id)
            setSuccessMessage("Expense deleted successfully!")
            setTimeout(() => {
                navigate("/expenses")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to delete expense. Please try again.")
            console.error(error)
            setDeleting(false)
        }
    }

    const handleCancel = () => {
        navigate(`/expenses/${id}`)
    }

    if (loading) {
        return (
            <section className="section-detail">
                <div className="detail-card detail-card-expense">
                    <p>Loading expense...</p>
                </div>
            </section>
        )
    }

    return (
        <section className="section-detail">
            <h1>Delete Expense</h1>

            {/* Confirmation Warning Message */}
            <div className="error-message" style={{
                backgroundColor: '#fff3cd',
                borderColor: '#ffc107',
                color: '#856404',
                marginBottom: '20px'
            }}>
                <strong>Warning:</strong> Are you sure you want to delete this expense? This action cannot be undone.
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

            {/* Display expense details (read-only) */}
            {expense ? (
                <div className="detail-card detail-card-expense">
                    <article>
                        <h2>{expense.category.name}</h2>
                        <p className="meta">
                            <strong>Amount:</strong> ${expense.amount}
                        </p>
                        <p>
                            <strong>Date:</strong> {expense.date}
                        </p>
                        <p>
                            <strong>Client:</strong> {expense.client?.name || 'No client provided.'}
                        </p>
                        <p>
                            <strong>Project:</strong> {expense.project?.name || 'No project provided.'}
                        </p>
                        <p>
                            <strong>Note:</strong> {expense.note || 'No note provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-expense">
                    <p>No expense found.</p>
                </div>
            )}

            {/* Action buttons */}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small-delete" onClick={handleCancel} disabled={deleting}>
                    Cancel
                </div>

                <div className="summary-pill summary-pill-small-delete" onClick={handleDelete} disabled={deleting}>
                    {deleting ? 'Deleting...' : 'Confirm Delete'}
                </div>
            </div>
        </section >
    )
}

export default DeleteExpense;
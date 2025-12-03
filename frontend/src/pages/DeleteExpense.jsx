import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchExpense, deleteExpense } from "../services/api";
import '../Transactions.css'

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
        return <p>Loading expense...</p>
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
                <article>
                    <h2>{expense.category.name}</h2>
                    <p className="meta">
                        <strong>Amount:</strong> ${expense.amount} · <strong>Date:</strong> {expense.date}
                    </p>
                    <p>{expense.note || 'No note provided.'}</p>
                </article>
            ) : (
                <p>No expense found.</p>
            )}

            {/* Action buttons */}
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                <button 
                    onClick={handleCancel}
                    disabled={deleting}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#6c757d',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: deleting ? 'not-allowed' : 'pointer'
                    }}
                >
                    Cancel
                </button>
                <button 
                    onClick={handleDelete}
                    disabled={deleting}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#dc3545',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: deleting ? 'not-allowed' : 'pointer'
                    }}
                >
                    {deleting ? 'Deleting...' : 'Confirm Delete'}
                </button>
            </div>
        </section>
    )
}

export default DeleteExpense;
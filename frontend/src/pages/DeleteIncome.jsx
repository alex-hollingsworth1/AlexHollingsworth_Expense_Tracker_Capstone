import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { deleteIncome , fetchIncome } from "../services/api";
import '../Transactions.css'

function DeleteIncome() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [income, setIncome] = useState(null)
    const [loading, setLoading] = useState(true)
    const [deleting, setDeleting] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)
    const [successMessage, setSuccessMessage] = useState(null)

    // Fetch the income data
    useEffect(() => {
        fetchIncome(id)
            .then((income) => {
                setIncome(income)
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch income: ", error)
                setErrorMessage("Failed to load income")
                setLoading(false)
            })
    }, [id])

    const handleDelete = async (e) => {
        e.preventDefault()
        setErrorMessage(null)
        setDeleting(true)

        try {
            await deleteIncome(id)
            setSuccessMessage("Income transaction deleted successfully!")
            setTimeout(() => {
                navigate("/income")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to delete income transaction. Please try again.")
            console.error(error)
            setDeleting(false)
        }
    }

    const handleCancel = () => {
        navigate(`/income/${id}`)
    }

    if (loading) {
        return <p>Loading income...</p>
    }

    return (
        <section className="section-detail">
            <h1>Delete Income Transaction</h1>

            {/* Confirmation Warning Message */}
            <div className="error-message" style={{
                backgroundColor: '#fff3cd',
                borderColor: '#ffc107',
                color: '#856404',
                marginBottom: '20px'
            }}>
                <strong>Warning:</strong> Are you sure you want to delete this income transaction? This action cannot be undone.
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

            {/* Display income details (read-only) */}
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

export default DeleteIncome;
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { deleteClient, fetchClient } from "../services/api";
import '../styles/Transactions.css'

function DeleteClient() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [client, setClient] = useState(null)
    const [loading, setLoading] = useState(true)
    const [deleting, setDeleting] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)
    const [successMessage, setSuccessMessage] = useState(null)

    // Fetch the client data
    useEffect(() => {
        fetchClient(id)
            .then((client) => {
                setClient(client)
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch client: ", error)
                setErrorMessage("Failed to load client")
                setLoading(false)
            })
    }, [id])

    const handleDelete = async (e) => {
        e.preventDefault()
        setErrorMessage(null)
        setDeleting(true)

        try {
            await deleteClient(id)
            setSuccessMessage("Client deleted successfully!")
            setTimeout(() => {
                navigate("/clients")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to delete client. Please try again.")
            console.error(error)
            setDeleting(false)
        }
    }

    const handleCancel = () => {
        navigate(`/clients/${id}`)
    }

    if (loading) {
        return (
            <section className="section-detail">
                <div className="detail-card detail-card-client">
                    <p>Loading client...</p>
                </div>
            </section>
        )
    }

    return (
        <section className="section-detail">
            <h1>Delete Client</h1>

            {/* Confirmation Warning Message */}
            <div className="error-message" style={{
                backgroundColor: '#fff3cd',
                borderColor: '#ffc107',
                color: '#856404',
                marginBottom: '20px'
            }}>
                <strong>Warning:</strong> Are you sure you want to delete this client? This action cannot be undone.
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

            {/* Display client details (read-only) */}
            {client ? (
                <div className="detail-card detail-card-client">
                    <article>
                        <h2>{client.name}</h2>
                        <p className="meta">
                            <strong>Email:</strong> {client.email}
                        </p>
                        <p>
                            <strong>Phone Number:</strong> {client.phone_number || 'No phone number provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-client">
                    <p>No client found.</p>
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

export default DeleteClient;
import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchClient } from '../services/api'
import '../styles/Transactions.css'

const ClientDetail = () => {
    const { id } = useParams()
    const [client, setClient] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchClient(id)
            .then(setClient)
            .catch((error) => {
                console.error("Failed to fetch client: ", error)
                setErrorMessage("Failed to load client")
            })
    }, [id])

    return (
        <section className="section-detail">
            <div style={{ textAlign: 'left', marginBottom: '1rem', marginLeft: '-1rem' }}>
                <Link
                    to="/clients"
                    className="summary-pill summary-pill-small"
                >
                    ← Back to Clients
                </Link>
            </div>
            <h1>Client Detail</h1>
            {errorMessage && (
                <div className="error-message">
                    {errorMessage}
                </div>
            )}
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
                    <p>Loading client details...</p>
                </div>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-client/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill-small-delete-red" onClick={() => navigate(`/delete-client/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default ClientDetail;

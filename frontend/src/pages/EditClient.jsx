import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchClient, updateClient } from "../services/api";
import '../styles/Create.css';

function EditClient() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [phoneNumber, setPhoneNumber] = useState("")
    const [loading, setLoading] = useState(true)
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    // Fetch the client data
    useEffect(() => {
        fetchClient(id)
            .then((client) => {
                // Pre-populate form fields
                if (client) {
                    setName(client.name)
                    setEmail(client.email)
                    setPhoneNumber(client.phone_number || "")
                }
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch client: ", error)
                setErrorMessage("Failed to load client")
                setLoading(false)
            })
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()

        const clientData = {
            name,
            email,
            phone_number: phoneNumber
        }

        try {
            await updateClient(id, clientData)
            setSuccessMessage("Client edited successfully!")
            setTimeout(() => {
                navigate("/clients")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to update client")
            console.error(error)
        }
    }

    if (loading) {
        return <p>Loading client...</p>
    }

    return (
        <section className="create-form-section">
            <h1>Edit Client</h1>
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
            <form onSubmit={handleSubmit} className="create-form">
                <div>
                    <input
                        type="text"
                        value={name || ''}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Client Name"
                        className={errors.name ? 'error' : ''}
                        required
                    />
                    {errors.name && <div className="field-error">{errors.name}</div>}
                </div>
                <div>
                    <label>
                        Email
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className={errors.email ? 'error' : ''}
                            placeholder="Email"
                        />
                    </label>

                    {errors.email && <div className="field-error">{errors.email}</div>}
                </div>
                <div>
                    <label>
                        Phone Number (optional)
                        <input
                            type="text"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                            className={errors.phoneNumber ? 'error' : ''}
                            placeholder="Phone Number (optional)"
                        />
                    </label>
                    {errors.phoneNumber && <div className="field-error">{errors.phoneNumber}</div>}
                </div>
                <button type="submit">Update Client</button>
            </form>
        </section>
    )
}

export default EditClient;


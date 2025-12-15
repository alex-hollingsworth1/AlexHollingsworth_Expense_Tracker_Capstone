import { useState } from 'react'
import { createClient } from '../services/api'
import '../Create.css'

function CreateClient() {
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [phoneNumber, setPhoneNumber] = useState("")
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    const resetForm = () => {
        setName("")
        setEmail("")
        setPhoneNumber("")
    }

    const validateForm = () => {
        const newErrors = {}

        // Validate name
        if (!name || name.trim() === "") {
            newErrors.name = "Please enter a client name."
        }

        // Validate email
        if (!email || email.trim() === "") {
            newErrors.email = "Please enter a valid email address."
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            newErrors.email = "Please enter a valid email address."
        }

        // Phone number is optional, so no validation needed

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        setErrors({})
        setErrorMessage(null)
        if (!validateForm()) {
            return
        }
        const clientData = {
            name,
            email,
            phone_number: phoneNumber || null
        }

        try {
            await createClient(clientData)
            setSuccessMessage("Client created successfully!")
            resetForm()
            setTimeout(() => {
                setSuccessMessage(null)
            }, 3000)
        } catch (error) {
            setErrorMessage("Failed to create client. Please try again.")
            console.error("Failed to create client:", error)
        }
    }

    return (
        <section className="create-form-section">
            <h1>Create Client</h1>
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
                <button type="submit">Create Client</button>
            </form>
        </section>
    )
}

export default CreateClient;
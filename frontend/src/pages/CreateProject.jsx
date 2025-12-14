import { useState, useEffect } from 'react'
import { createProject, fetchClients } from '../services/api'
import '../Create.css'

function CreateProject() {
    const [name, setName] = useState("")
    const [dateCreated, setDateCreated] = useState("")
    const [note, setNote] = useState("")
    const [client, setClient] = useState("")
    const [clients, setClients] = useState([])
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    useEffect(() => {
        fetchClients()
            .then(setClients)
            .catch(console.error)
    }, [])

    const resetForm = () => {
        setName("")
        setDateCreated("")
        setNote("")
        setClient("")
    }

    const validateForm = () => {
        const newErrors = {}

        // Validate name
        if (!name || name.trim() === "") {
            newErrors.name = "Please enter a project name."
        }

        // Validate date created
        if (!dateCreated) {
            newErrors.dateCreated = "Please select a creation date."
        }

        // Validate client
        if (!client || client.trim() === "") {
            newErrors.client = "Please select a client."
        }

        // Validate note length (if provided)
        if (note && note.length > 250) {
            newErrors.note = "Note must be 250 characters or less."
        }


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
        const projectData = {
            name,
            date_created: dateCreated,
            client_id: parseInt(client),
            note: note || null
        }

        try {
            const createdProject = await createProject(projectData)
            setSuccessMessage("Project created successfully!")
            resetForm()
            setTimeout(() => {
                setSuccessMessage(null)
            }, 3000)
        } catch (error) {
            setErrorMessage("Failed to create project. Please try again.")
            console.error("Failed to create project:", error)
        }
    }



    return (
        <section className="create-form-section">
            <h1>Create Project</h1>
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
                        placeholder="Project Name"
                        className={errors.name ? 'error' : ''}
                        required
                    />
                    {errors.name && <div className="field-error">{errors.name}</div>}
                </div>
                <div>
                    <label>
                        Date Created
                        <input
                            type="date"
                            value={dateCreated}
                            onChange={(e) => setDateCreated(e.target.value)}
                            className={errors.dateCreated ? 'error' : ''}
                            required
                        />
                    </label>
                    {errors.dateCreated && <div className="field-error">{errors.dateCreated}</div>}
                </div>
                <div>
                    <select
                        value={client}
                        onChange={(e) => setClient(e.target.value)}
                        className={errors.client ? 'error' : ''}
                        required
                    >
                        <option value="">Select a client</option>
                        {clients.map((client) => (
                            <option key={client.id} value={client.id}>{client.name}</option>
                        ))}
                    </select>
                    {errors.client && <div className="field-error">{errors.client}</div>}
                </div>
                <div>
                    <label>
                        Note (optional)
                        <input
                            type="text"
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            className={errors.note ? 'error' : ''}
                            placeholder="Note (optional)"
                        />
                    </label>

                    {errors.note && <div className="field-error">{errors.note}</div>}
                </div>
                <button type="submit">Create Project</button>
            </form>
        </section>
    )
}

export default CreateProject;
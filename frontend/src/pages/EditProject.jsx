import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchProject, updateProject, fetchClients } from "../services/api";
import '../styles/Create.css';

function EditProject() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [name, setName] = useState("")
    const [dateCreated, setDateCreated] = useState("")
    const [client, setClient] = useState("")
    const [clients, setClients] = useState([])
    const [note, setNote] = useState("")
    const [loading, setLoading] = useState(true)
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    // Fetch the clients
    useEffect(() => {
        fetchClients()
        .then(setClients)
        .catch(console.error)
    }, [])

    // Fetch the project data
    useEffect(() => {
        fetchProject(id)
        .then((project) => {
            // Pre-populate form fields
            if (project) {
                setName(project.name)
                setDateCreated(project.date_created)
                setClient(project.client?.id || "")
                setNote(project.note || "")
            }
            setLoading(false)
        })
        .catch((error) => {
            console.error("Failed to fetch project: ", error)
            setErrorMessage("Failed to load project")
            setLoading(false)
        })
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()

        const projectData = {
            name,
            date_created: dateCreated,
            client_id: parseInt(client),
            note: note || null
        }

        try {
            await updateProject(id, projectData)
            setSuccessMessage("Project edited successfully!")
            setTimeout(() => {
                navigate("/projects")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to update project")
            console.error(error)
        }
    }

    if (loading) {
        return <p>Loading project...</p>
    }

    return (
        <section className="create-form-section">
            <h1>Edit Project</h1>
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
                <button type="submit">Update Project</button>
            </form>
        </section>
    )
}

export default EditProject;


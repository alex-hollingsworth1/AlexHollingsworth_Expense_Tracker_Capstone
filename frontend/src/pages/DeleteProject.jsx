import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { deleteProject, fetchProject } from "../services/api";
import '../Transactions.css'

function DeleteProject() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [project, setProject] = useState(null)
    const [loading, setLoading] = useState(true)
    const [deleting, setDeleting] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)
    const [successMessage, setSuccessMessage] = useState(null)

    // Fetch the project data
    useEffect(() => {
        fetchProject(id)
            .then((project) => {
                setProject(project)
                setLoading(false)
            })
            .catch((error) => {
                console.error("Failed to fetch project: ", error)
                setErrorMessage("Failed to load project")
                setLoading(false)
            })
    }, [id])

    const handleDelete = async (e) => {
        e.preventDefault()
        setErrorMessage(null)
        setDeleting(true)

        try {
            await deleteProject(id)
            setSuccessMessage("Project deleted successfully!")
            setTimeout(() => {
                navigate("/projects")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to delete project. Please try again.")
            console.error(error)
            setDeleting(false)
        }
    }

    const handleCancel = () => {
        navigate(`/project/${id}`)
    }

    if (loading) {
        return (
            <section className="section-detail">
                <div className="detail-card detail-card-project">
                    <p>Loading project...</p>
                </div>
            </section>
        )
    }

    return (
        <section className="section-detail">
            <h1>Delete Project</h1>

            {/* Confirmation Warning Message */}
            <div className="error-message" style={{
                backgroundColor: '#fff3cd',
                borderColor: '#ffc107',
                color: '#856404',
                marginBottom: '20px'
            }}>
                <strong>Warning:</strong> Are you sure you want to delete this project? This action cannot be undone.
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

            {/* Display project details (read-only) */}
            {project ? (
                <div className="detail-card detail-card-project">
                    <article>
                        <h2>{project.name}</h2>
                        <p className="meta">
                            <strong>Client:</strong> {project.client?.name || 'No client provided.'}
                        </p>
                        <p>
                            <strong>Date Created:</strong> {project.date_created}
                        </p>
                        <p>
                            <strong>Note:</strong> {project.note || 'No note provided.'}
                        </p>
                    </article>
                </div>
            ) : (
                <div className="detail-card detail-card-project">
                    <p>No project found.</p>
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

export default DeleteProject;
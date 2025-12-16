import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchProject } from '../services/api'
import '../styles/Transactions.css'

const ProjectDetail = () => {
    const { id } = useParams()
    const [project, setProject] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchProject(id)
            .then(setProject)
            .catch(console.error)
    }, [id])

    return (
        <section className="section-detail">
            <div style={{ textAlign: 'left', marginBottom: '1rem', marginLeft: '-1rem' }}>
                <Link
                    to="/projects"
                    className="summary-pill summary-pill-small"
                >
                    ← Back to Projects
                </Link>
            </div>
            <h1>Project Detail</h1>
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
                    <p>Loading project details...</p>
                </div>
            )}
            <div className="action-buttons-container">
                <div className="summary-pill summary-pill-small" onClick={() => navigate(`/edit-project/${id}`)}>
                    Edit
                </div>
                <div className="summary-pill-small-delete-red" onClick={() => navigate(`/delete-project/${id}`)}>
                    Delete
                </div>
            </div>
        </section>
    )
}

export default ProjectDetail;

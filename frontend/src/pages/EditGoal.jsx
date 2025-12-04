import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchGoal, updateGoal } from "../services/api";
import '../Create.css';

function EditGoal() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [editGoal, setEditGoal] = useState(null)
    const [name, setName] = useState("")
    const [target, setTarget] = useState(null)
    const [deadline, setDeadline] = useState("")
    const [status, setStatus] = useState("Not Started")
    const [note, setNote] = useState("")
    const [loading, setLoading] = useState(true)
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)

    // Fetch the goal data
    useEffect(() => {
        fetchGoal(id)
        .then((goal) => {
            setEditGoal(goal)
            // Pre-populate form fields
            if (goal) {
                setName(goal.name)
                setTarget(goal.target)
                setDeadline(goal.deadline)
                setStatus(goal.status)
                setNote(goal.note || "")
            }
            setLoading(false)
        })
        .catch((error) => {
            console.error("Failed to fetch goal: ", error)
            setErrorMessage("Failed to load goal")
            setLoading(false)
        })
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()

        const goalData = {
            name,
            target: parseFloat(target),
            deadline,
            status,
            note: note || null
        }

        try {
            const updatedGoal = await updateGoal(id, goalData)
            setSuccessMessage("Goal edited successfully!")
            setTimeout(() => {
                navigate("/goals")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to update goal")
            console.error(error)
        }
    }

    if (loading) {
        return <p>Loading goal...</p>
    }

    return (
        <section className="create-form-section">
            <h1>Edit Goal</h1>
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
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Goal Name"
                    required
                />
                <input
                    type="number"
                    value={target || ''}
                    onChange={(e) => setTarget(e.target.value)}
                    placeholder="Target Amount"
                    required
                />
                <label>
                    Deadline
                    <input
                        type="date"
                        value={deadline}
                        onChange={(e) => setDeadline(e.target.value)}
                        required
                    />
                </label>
                <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    required
                >
                    <option value="Not Started">Not Started</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                </select>
                <input
                    type="text"
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    placeholder="Note (optional)"
                />
                <button type="submit">Edit Goal</button>
            </form>
        </section>
    )
}

export default EditGoal;


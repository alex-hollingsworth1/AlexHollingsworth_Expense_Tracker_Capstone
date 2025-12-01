import { useState } from 'react'
import { createGoal } from '../services/api'
import '../Create.css'

function CreateGoal() {
    const [name, setName] = useState("")
    const [target, setTarget] = useState(null)
    const [deadline, setDeadline] = useState("")
    const [note, setNote] = useState("")
    const [status, setStatus] = useState("Not Started")
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)

    const resetForm = () => {
        setName("")
        setTarget(null)
        setDeadline("")
        setNote("")
        setStatus("Not Started")
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setSuccessMessage(null)
        setErrorMessage(null)

        const goalData = {
            name,
            target: parseFloat(target),
            deadline,
            note: note || null,
            status
        }

        try {
            const createdGoal = await createGoal(goalData)
            setSuccessMessage("Goal created successfully!")
            resetForm()
            setTimeout(() => {
                setSuccessMessage(null)
            }, 3000)
        } catch (error) {
            setErrorMessage("Failed to create goal. Please try again.")
            console.error("Failed to create goal:", error)
        }
    }

    return (
        <section className="create-form-section">
            <h1>Create New Goal</h1>
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
                <button type="submit">Create Goal</button>
            </form>
        </section>
    )
}

export default CreateGoal;


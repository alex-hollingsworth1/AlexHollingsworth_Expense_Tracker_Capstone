import { useState } from 'react'
import { createGoal } from '../services/api'
import '../styles/Create.css'

function CreateGoal() {
    const [name, setName] = useState("")
    const [target, setTarget] = useState(null)
    const [deadline, setDeadline] = useState("")
    const [note, setNote] = useState("")
    const [status, setStatus] = useState("Not Started")
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    const resetForm = () => {
        setName("")
        setTarget(null)
        setDeadline("")
        setNote("")
        setStatus("Not Started")
    }

    const validateForm = () => {
        const newErrors = {}

        // Validate name
        if (!name || name.trim() === "") {
            newErrors.name = "Please enter a goal name."
        }

        // Validate target
        if (!target || target === "" || parseFloat(target) <= 0) {
            newErrors.target = "Target must be greater than 0."
        }

        // Validate deadline
        if (!deadline) {
            newErrors.deadline = "Please select a deadline."
        }

        // Validate status (check if it's one of the valid options)
        const validStatuses = ["Not Started", "In Progress", "Completed"]
        if (!status || !validStatuses.includes(status)) {
            newErrors.status = "Please select a valid status."
        }

        // Validate note length (if provided)
        if (note && note.length > 250) {
            newErrors.note = "Note must be 250 characters or less"
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0  // Returns true if no errors

    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setSuccessMessage(null)

        // Clear errors
        setErrors({})
        setErrorMessage(null)

        // Validate form
        if (!validateForm()) {
            return
        }

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
        <div>
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
                    <div>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className={errors.name ? 'error' : ''}
                            placeholder="Goal Name"
                            required
                        />
                        {errors.name && <div className="field-error">{errors.name}</div>}
                    </div>

                    <div>
                        <input
                            type="number"
                            value={target || ''}
                            onChange={(e) => setTarget(e.target.value)}
                            className={errors.target ? 'error' : ''}
                            placeholder="Target Amount"
                            required
                        />
                        {errors.target && <div className="field-error">{errors.target}</div>}
                    </div>

                    <div>
                        <label>
                            Deadline
                            <input
                                type="date"
                                value={deadline}
                                onChange={(e) => setDeadline(e.target.value)}
                                className={errors.deadline ? 'error' : ''}
                                required
                            />
                            {errors.deadline && <div className="field-error">{errors.deadline}</div>}
                        </label>
                    </div>

                    <div>
                        <select
                            value={status}
                            onChange={(e) => setStatus(e.target.value)}
                            className={errors.status ? 'error' : ''}
                            required
                        >
                            <option value="Not Started">Not Started</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                        </select>
                        {errors.status && <div className="field-error">{errors.status}</div>}
                    </div>

                    <div>
                        <input
                            type="text"
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            className={errors.note ? 'error' : ''}
                            placeholder="Note (optional)"
                        />
                        {errors.note && <div className="field-error">{errors.note}</div>}
                    </div>

                    <button type="submit">Create Goal</button>
                </form>
            </section>
        </div>

    )
}

export default CreateGoal;


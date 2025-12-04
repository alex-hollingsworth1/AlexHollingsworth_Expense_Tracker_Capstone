import { useState, useEffect } from 'react'
import { createBudget, fetchCategories } from '../services/api'
import '../Create.css'

function CreateBudget() {
    const [amount, setAmount] = useState(null)
    const [startDate, setStartDate] = useState("")
    const [endDate, setEndDate] = useState("")
    const [category, setCategory] = useState("")
    const [categories, setCategories] = useState([])
    const [note, setNote] = useState("")
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    useEffect(() => {
        fetchCategories()
            .then(setCategories)
            .catch(console.error)
    }, [])

    const resetForm = () => {
        setAmount(null)
        setStartDate("")
        setEndDate("")
        setCategory("")
        setNote("")
    }

    const validateForm = () => {
        const newErrors = {}

        // Validate amount
        if (!amount || amount === "" || parseFloat(amount) <= 0) {
            newErrors.amount = "Amount must be greater than 0."
        }

        // Validate start date
        if (!startDate) {
            newErrors.startDate = "Please select a start date."
        }

        // Validate end date
        if (!endDate) {
            newErrors.endDate = "Please select an end date."
        }

        // Validate that end date is after start date
        if (startDate && endDate && new Date(endDate) <= new Date(startDate)) {
            newErrors.endDate = "End date must be after start date."
        }

        // Validate category
        if (!category || category === '') {
            newErrors.category = "Please select a category"
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

        const budgetData = {
            amount: parseFloat(amount),
            start_date: startDate,
            end_date: endDate,
            category_id: parseInt(category),
            note: note || null
        }

        try {
            const createdBudget = await createBudget(budgetData)
            setSuccessMessage("Budget created successfully!")
            resetForm()
            setTimeout(() => {
                setSuccessMessage(null)
            }, 3000)
        } catch (error) {
            setErrorMessage("Failed to create budget. Please try again.")
            console.error("Failed to create budget:", error)
        }
    }

    return (
        <div>
            <section className="create-form-section">
                <h1>Create New Budget</h1>
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
                            type="number"
                            value={amount || ''}
                            onChange={(e) => setAmount(e.target.value)}
                            placeholder="Amount"
                            className={errors.amount ? 'error' : ''}
                            required
                        />
                        {errors.amount && <div className="field-error">{errors.amount}</div>}
                    </div>

                    <div>
                        <label>
                            Start Date
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className={errors.startDate ? 'error' : ''}
                                required
                            />
                            {errors.startDate && <div className="field-error">{errors.startDate}</div>}
                        </label>
                    </div>

                    <div>
                        <label>
                            End Date
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className={errors.endDate ? 'error' : ''}
                                required
                            />
                            {errors.endDate && <div className="field-error">{errors.endDate}</div>}
                        </label>
                    </div>

                    <div>
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className={errors.category ? 'error' : ''}
                            required
                        >
                            <option value="">Select a category</option>
                            {categories.map((cat) => (
                                <option key={cat.id} value={cat.id}>{cat.name}</option>
                            ))}
                        </select>
                        {errors.category && <div className="field-error">{errors.category}</div>}
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
                    <button type="submit">Create Budget</button>
                </form>
            </section>
        </div>
    )
}

export default CreateBudget;


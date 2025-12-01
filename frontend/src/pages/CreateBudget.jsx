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

    const handleSubmit = async (e) => {
        e.preventDefault()
        setSuccessMessage(null)
        setErrorMessage(null)

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
                <input
                    type="number"
                    value={amount || ''}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount"
                    required
                />
                <label>
                    Start Date
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                        required
                    />
                </label>
                <label>
                    End Date
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        required
                    />
                </label>
                <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    required
                >
                    <option value="">Select a category</option>
                    {categories.map((cat) => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                </select>
                <input
                    type="text"
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    placeholder="Note (optional)"
                />
                <button type="submit">Create Budget</button>
            </form>
        </section>
    )
}

export default CreateBudget;


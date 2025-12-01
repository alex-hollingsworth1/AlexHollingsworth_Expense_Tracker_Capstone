import { useState, useEffect } from 'react'
import { createExpense, fetchCategories } from '../services/api'
import '../Create.css'

function CreateExpense() {
    const [amount, setAmount] = useState(null)
    const [date, setDate] = useState("")
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
        setDate("")
        setCategory("")
        setNote("")
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        const expenseData = {
            amount: parseFloat(amount),
            date,
            category_id: parseInt(category),
            note: note || null
        }

        try {
            const createdExpense = await createExpense(expenseData)
            setSuccessMessage("Expense created successfully!")
            resetForm()
            setTimeout(() => {
                setSuccessMessage(null)
            }, 3000)
        } catch (error) {
            setErrorMessage("Failed to create expense. Please try again.")
            console.error("Failed to create expense:", error)
        }
    }



    return (
        <section className="create-form-section">
            <h1>Create New Expense</h1>
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
                    Date
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
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
                <button type="submit">Create Expense</button>
            </form>
        </section>
    )
}

export default CreateExpense;
import { useState, useEffect } from 'react'
import { createIncome, fetchCategories } from '../services/api'
import '../Create.css'

function CreateIncome() {
    const [amount, setAmount] = useState(null)
    const [date, setDate] = useState("")
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
        setDate("")
        setCategory("")
        setNote("")
    }

    const validateForm = () => {
        const newErrors = {}

        // Validate amount
        if (!amount || amount === "" || parseFloat(amount) <= 0) {
            newErrors.amount = "Amount must be greater than 0."
        }

        // Validate date
        if (!date) {
            newErrors.date = "Please select a date."
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

        // Clear errors
        setErrors({})
        setErrorMessage(null)

        // Validate form
        if (!validateForm()) {
            return
        }

        const incomeData = {
            amount: parseFloat(amount),
            date,
            category_id: parseInt(category),
            note: note || null
        }

        try {
            const createdIncome = await createIncome(incomeData)
            setSuccessMessage("Income logged successfully!")
            resetForm()
            setTimeout(() => {
                setSuccessMessage(null)
            }, 3000)
        } catch (error) {
            setErrorMessage("Failed to create income transaction. Please try again.")
            console.error("Failed to create income transaction:", error)
        }
    }



    return (
        <section className="create-form-section">
            <h1>Create Income Transaction</h1>
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
                    <label>
                        Date Paid
                        <input
                            type="date"
                            value={date}
                            onChange={(e) => setDate(e.target.value)}
                            className={errors.date ? 'error' : ''}
                            required
                        />
                    </label>
                    {errors.date && <div className="field-error">{errors.date}</div>}
                </div>

                <div>
                    <input
                        type="text"
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                        placeholder="Note (optional)"
                        className={errors.note ? 'error' : ''}
                    />
                    {errors.note && <div className="field-error">{errors.note}</div>}
                </div>
                
                <button type="submit">Create Income</button>
            </form>
        </section>
    )
}

export default CreateIncome;
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchExpense, fetchCategories, updateExpense } from "../services/api";

function EditExpense() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [editExpense, setEditExpense] = useState(null)
    const [amount, setAmount] = useState(null)
    const [date, setDate] = useState("")
    const [category, setCategory] = useState("")
    const [categories, setCategories] = useState([])
    const [note, setNote] = useState("")
    const [loading, setLoading] = useState(true)
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)

    // Fetch the categories

    useEffect(() => {
        fetchCategories()
        .then(setCategories)
        .catch(console.error)
    }, [])

    // Fetch the expense data
    useEffect(() => {
        fetchExpense(id)
        .then((expense) => {
            setEditExpense(expense)
            // Pre-populate form fields
            if (expense) {
                setAmount(expense.amount)
                setDate(expense.date)
                setCategory(expense.category.id)
                setNote(expense.note || "")
            }
            setLoading(false)
        })
        .catch((error) => {
            console.error("Failed to fetch expense: ", error)
            setErrorMessage("Failed to load expense")
            setLoading(false)
        })
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()

        const expenseData = {
            amount: parseFloat(amount),
            date,
            category_id: parseInt(category),
            note: note || null
        }

        try {
            const updatedExpense = await updateExpense(id, expenseData)
            setSuccessMessage("Expense edited successfully!")
            setTimeout(() => {
                navigate("/expenses")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to update expense")
            console.error(error)
        }
    }

    return (
        <section className="create-form-section">
            <h1>Edit Expense</h1>
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
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    placeholder="Date"
                    required
                />
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
                <button type="submit">Edit Expense</button>
            </form>
        </section>
    )
}

export default EditExpense;


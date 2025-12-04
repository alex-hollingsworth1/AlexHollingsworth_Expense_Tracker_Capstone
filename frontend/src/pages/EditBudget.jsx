import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchBudget, fetchCategories, updateBudget } from "../services/api";
import '../Create.css';

function EditBudget() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [editBudget, setEditBudget] = useState(null)
    const [amount, setAmount] = useState(null)
    const [startDate, setStartDate] = useState("")
    const [endDate, setEndDate] = useState("")
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

    // Fetch the budget data
    useEffect(() => {
        fetchBudget(id)
        .then((budget) => {
            setEditBudget(budget)
            // Pre-populate form fields
            if (budget) {
                setAmount(budget.amount)
                setStartDate(budget.start_date)
                setEndDate(budget.end_date)
                setCategory(budget.category.id)
                setNote(budget.note || "")
            }
            setLoading(false)
        })
        .catch((error) => {
            console.error("Failed to fetch budget: ", error)
            setErrorMessage("Failed to load budget")
            setLoading(false)
        })
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()

        const budgetData = {
            amount: parseFloat(amount),
            start_date: startDate,
            end_date: endDate,
            category_id: parseInt(category),
            note: note || null
        }

        try {
            const updatedBudget = await updateBudget(id, budgetData)
            setSuccessMessage("Budget edited successfully!")
            setTimeout(() => {
                navigate("/budgets")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to update budget")
            console.error(error)
        }
    }

    if (loading) {
        return <p>Loading budget...</p>
    }

    return (
        <section className="create-form-section">
            <h1>Edit Budget</h1>
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
                <button type="submit">Edit Budget</button>
            </form>
        </section>
    )
}

export default EditBudget;


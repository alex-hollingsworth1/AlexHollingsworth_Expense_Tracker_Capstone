import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchIncome, fetchCategories, updateIncome } from "../services/api";
import '../Create.css';

function EditIncome() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [editIncome, setEditIncome] = useState(null)
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

    // Fetch the income data
    useEffect(() => {
        fetchIncome(id)
        .then((income) => {
            setEditIncome(income)
            // Pre-populate form fields
            if (income) {
                setAmount(income.amount)
                setDate(income.date)
                setCategory(income.category.id)
                setNote(income.note || "")
            }
            setLoading(false)
        })
        .catch((error) => {
            console.error("Failed to fetch income: ", error)
            setErrorMessage("Failed to load income")
            setLoading(false)
        })
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()

        const incomeData = {
            amount: parseFloat(amount),
            date,
            category_id: parseInt(category),
            note: note || null
        }

        try {
            const updatedIncome = await updateIncome(id, incomeData)
            setSuccessMessage("Income edited successfully!")
            setTimeout(() => {
                navigate("/income")
            }, 750)
        } catch (error) {
            setErrorMessage("Failed to update income")
            console.error(error)
        }
    }

    if (loading) {
        return <p>Loading income...</p>
    }

    return (
        <section className="create-form-section">
            <h1>Edit Income</h1>
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
                    Date Paid
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
                <button type="submit">Edit Income</button>
            </form>
        </section>
    )
}

export default EditIncome;


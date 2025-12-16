import { useState, useEffect } from 'react'
import { createIncome, fetchCategories, createCategory } from '../services/api'
import '../styles/Create.css'

function CreateIncome() {
    const [amount, setAmount] = useState(null)
    const [date, setDate] = useState("")
    const [category, setCategory] = useState("")
    const [addCategory, setAddCategory] = useState(false)
    const [newCategoryName, setNewCategoryName] = useState("")
    const [categories, setCategories] = useState([])
    const [note, setNote] = useState("")
    const [successMessage, setSuccessMessage] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const [errors, setErrors] = useState({})

    useEffect(() => {
        fetchCategories('INCOME')
            .then(setCategories)
            .catch(console.error)
    }, [addCategory])

    const resetForm = () => {
        setAmount(null)
        setDate("")
        setCategory("")
        setNote("")
    }

    const handleNewCategory = async (category_name) => {
        // Validate category name
        if (!category_name || category_name.trim() === '') {
            setErrors({...errors, category: "Category name is required"})
            return
        }
    
        try {
            // Create category data
            const categoryData = {
                'name': category_name.trim(),
                'category_type': 'INCOME'
            }
    
            // Create the category
            const createdCategory = await createCategory(categoryData)
    
            // Refresh categories list
            const updatedCategories = await fetchCategories('INCOME')
            setCategories(updatedCategories)
    
            // Set the newly created category as selected
            setCategory(createdCategory.id.toString())
            
            // Clear the new category name input
            setNewCategoryName("")
            
            // Close the add category input
            setAddCategory(false)
    
        } catch (error) {
            setErrorMessage("Failed to create category. Please try again.")
            console.error("Failed to create category:", error)
        }
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
                    {addCategory ? (
                        <div>
                            <input
                                type="text"
                                value={newCategoryName}
                                onChange={(e) => setNewCategoryName(e.target.value)}
                                placeholder="Enter new category name"
                            />
                            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                                <button 
                                    type="button" 
                                    onClick={() => handleNewCategory(newCategoryName)} 
                                    className="btn-add-category"
                                >
                                    Add Category
                                </button>
                                <button 
                                    type="button" 
                                    onClick={() => {
                                        setAddCategory(false)
                                        setNewCategoryName("")
                                    }} 
                                    className="btn-cancel"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>
                    ) : (
                        <select
                            value={category}
                            onChange={(e) => {
                                if (e.target.value === "add_new") {
                                    setAddCategory(true)
                                    setCategory("")
                                } else {
                                    setCategory(e.target.value)
                                }
                            }}
                            className={errors.category ? 'error': ''}
                            required
                        >
                            <option value="">Select a category</option>
                            {categories.map((cat) => (
                                <option key={cat.id} value={cat.id}>{cat.name}</option>
                            ))}
                            <option value="add_new">➕ Add New Category</option>
                        </select>
                    )}
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
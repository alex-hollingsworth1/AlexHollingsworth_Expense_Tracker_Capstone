import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchExpenses, fetchCategories } from '../services/api'
import FilterBar from '../components/FilterBar'
import '../Transactions.css'

function ExpenseList() {

  // const [expenses, setExpenses] = useState([])
  const [categories, setCategories] = useState([])

  // Filter state
  const [filters, setFilters] = useState({
    category: '',
    dateFrom: '',
    dateTo: '',
    amountMin: '',
    amountMax: '',
    searchText: '',
    sortBy: 'date',
    sortOrder: 'desc'
  })

  // Original data (from API)
  const [allExpenses, setAllExpenses] = useState([])

  // Filtered/displayed data
  const [filteredExpenses, setFilteredExpenses] = useState([])

  useEffect(() => {
    fetchExpenses()
      .then(setAllExpenses)
      .catch(console.error)

    fetchCategories('EXPENSE')
      .then(setCategories)
      .catch(console.error)
  }, [])

  useEffect(() => {
    applyFilters()
  }, [allExpenses, filters])

  // Handler that updates filters state
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  const applyFilters = () => {
    let filtered = [...allExpenses]

    if (filters.category && filters.category !== 'all') {
      filtered = filtered.filter((expense) => {
        return expense.category.id === parseInt(filters.category)
      })
    }

    if (filters.dateFrom) {
      filtered = filtered.filter((expense) => {
        return expense.date >= filters.dateFrom
      })
    }

    if (filters.dateTo) {
      filtered = filtered.filter((expense) => {
        return expense.date <= filters.dateTo
      })
    }

    if (filters.amountMin) {
      filtered = filtered.filter((expense) => {
        return parseFloat(expense.amount) >= parseFloat(filters.amountMin)
      })
    }

    if (filters.amountMax) {
      filtered = filtered.filter((expense) => {
        return parseFloat(expense.amount) <= parseFloat(filters.amountMax)
      })
    }

    if (filters.searchText) {
      filtered = filtered.filter((expense) => {
        return expense.note?.toLowerCase().includes(filters.searchText.toLowerCase())
      })
    }

    if (filters.sortBy == 'date') {
      filtered.sort((a, b) => {
        const dateA = new Date(a.date)
        const dateB = new Date(b.date)
        const comparison = dateA - dateB
        return filters.sortOrder === 'desc' ? -comparison : comparison
      })
    }

    if (filters.sortBy == 'amount') {
      filtered.sort((a, b) => {
        const amountA = parseFloat(a.amount)
        const amountB = parseFloat(b.amount)
        const comparison = amountA - amountB
        return filters.sortOrder === 'desc' ? -comparison : comparison
      })
    }

    setFilteredExpenses(filtered)
  }


  return (
    <section className="section-listing">
      <h1>Expenses</h1>

      <FilterBar
        filters={filters}
        onFilterChange={handleFilterChange}
        categories={categories}
      />

      {filteredExpenses.length > 0 ? (
        <ul>
          {filteredExpenses.map((expense) => (
            <li key={expense.id}>
              <Link to={`/expenses/${expense.id}`}>
                <article className="expense-item">
                  <h2>{expense.category.name}</h2>
                  <p className="meta">
                    <strong>Date:</strong> {expense.date} · <strong>Amount:</strong> ${expense.amount}
                  </p>
                  <p>{expense.note || 'No note provided.'}</p>
                </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No expenses yet.</p>
      )}
    </section>
  )
}

export default ExpenseList;


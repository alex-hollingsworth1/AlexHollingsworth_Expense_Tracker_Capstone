import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchBudgets, fetchCategories } from '../services/api'
import FilterBar from '../components/FilterBar'
import '../Transactions.css'

function BudgetList() {
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
  const [allBudgets, setAllBudgets] = useState([])

  // Filtered/displayed data
  const [filteredBudgets, setFilteredBudgets] = useState([])

  useEffect(() => {
    fetchBudgets()
      .then(setAllBudgets)
      .catch(console.error)

    fetchCategories()
      .then(setCategories)
    .catch(console.error)
  }, [])

  useEffect(() => {
    applyFilters()
  }, [allBudgets, filters])

  // Handler that updates filters state
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  const applyFilters = () => {
    let filtered = [...allBudgets]

    // Filter by category
    if (filters.category && filters.category !== 'all') {
      filtered = filtered.filter((budget) => {
        return budget.category.id === parseInt(filters.category)
      })
    }

    // Filter by start date (From Start Date)
    if (filters.dateFrom) {
      filtered = filtered.filter((budget) => {
        return budget.start_date >= filters.dateFrom
      })
    }

    // Filter by end date (To End Date)
    if (filters.dateTo) {
      filtered = filtered.filter((budget) => {
        return budget.end_date <= filters.dateTo
      })
    }

    // Filter by min amount
    if (filters.amountMin) {
      filtered = filtered.filter((budget) => {
        return parseFloat(budget.amount) >= parseFloat(filters.amountMin)
      })
    }

    // Filter by max amount
    if (filters.amountMax) {
      filtered = filtered.filter((budget) => {
        return parseFloat(budget.amount) <= parseFloat(filters.amountMax)
      })
    }

    // Filter by note (search text)
    if (filters.searchText) {
      filtered = filtered.filter((budget) => {
        return budget.note?.toLowerCase().includes(filters.searchText.toLowerCase())
      })
    }

    // Sort by amount
    if (filters.sortBy === 'amount') {
      filtered.sort((a, b) => {
        const amountA = parseFloat(a.amount)
        const amountB = parseFloat(b.amount)
        const comparison = amountA - amountB
        return filters.sortOrder === 'desc' ? -comparison : comparison
      })
    }

    // Sort by start date
    if (filters.sortBy === 'date') {
      filtered.sort((a, b) => {
        const dateA = new Date(a.start_date)
        const dateB = new Date(b.start_date)
        const comparison = dateA - dateB
        return filters.sortOrder === 'desc' ? -comparison : comparison
      })
    }

    setFilteredBudgets(filtered)
  }

  // Filter categories to only show EXPENSE categories (budgets are for expenses)
  const expenseCategories = categories.filter(cat => cat.category_type === 'EXPENSE')

  return (
    <section className="section-listing">
      <h1>Budgets</h1>

      <FilterBar
        filters={filters}
        onFilterChange={handleFilterChange}
        categories={expenseCategories}
      />

      {filteredBudgets.length > 0 ? (
        <ul>
          {filteredBudgets.map((budget) => (
            <li key={budget.id}>
              <Link to={`/budgets/${budget.id}`}>
              <article>
                <h2>{budget.category.name}</h2>
                <p className="meta">
                  <strong>Amount:</strong> ${budget.amount} · <strong>Period:</strong> {budget.start_date} to {budget.end_date}
                </p>
                <p>{budget.note || 'No note provided.'}</p>
              </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No budgets yet.</p>
      )}
    </section>
  )
}

export default BudgetList


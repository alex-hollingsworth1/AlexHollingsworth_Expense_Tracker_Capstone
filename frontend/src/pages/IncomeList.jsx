import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchIncomes, fetchCategories } from '../services/api'
import FilterBar from '../components/FilterBar'
import '../Transactions.css'

function IncomeList() {
  // const [incomes, setIncomes] = useState([])
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
  const [allIncome, setAllIncome] = useState([])

  // Filtered/displayed data
  const [filteredIncome, setFilteredIncome] = useState([])

  useEffect(() => {
    fetchIncomes()
      .then(setAllIncome)
      .catch(console.error)

    fetchCategories()
      .then(setCategories)
      .catch(console.error)
  }, [])

  useEffect(() => {
    applyFilters()
  }, [allIncome, filters])

  // Handler that updates filters state
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  const applyFilters = () => {
    let filtered = [...allIncome]

    if (filters.category && filters.category !== 'all') {
      filtered = filtered.filter((income) => {
        return income.category.id === parseInt(filters.category)
      })
    }

    if (filters.dateFrom) {
      filtered = filtered.filter((income) => {
        return income.date >= filters.dateFrom
      })
    }

    if (filters.dateTo) {
      filtered = filtered.filter((income) => {
        return income.date <= filters.dateTo
      })
    }

    if (filters.amountMin) {
      filtered = filtered.filter((income) => {
        return parseFloat(income.amount) >= parseFloat(filters.amountMin)
      })
    }

    if (filters.amountMax) {
      filtered = filtered.filter((income) => {
        return parseFloat(income.amount) <= parseFloat(filters.amountMax)
      })
    }

    if (filters.searchText) {
      filtered = filtered.filter((income) => {
        return income.note?.toLowerCase().includes(filters.searchText.toLowerCase())
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

    setFilteredIncome(filtered)
  }

    return (
      <section className="section-listing">
        <h1>Income</h1>

        <FilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          categories={categories}
        />

        {filteredIncome.length > 0 ? (
          <ul>
            {filteredIncome.map((income) => (
              <li key={income.id}>
                <Link to={`/income/${income.id}`}>
                  <article>
                    <h2>{income.category.name}</h2>
                    <p className="meta">
                      <strong>Date:</strong> {income.date} · <strong>Amount:</strong> ${income.amount}
                    </p>
                    <p>{income.note || 'No note provided.'}</p>
                  </article>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p>No income yet.</p>
        )}
      </section>
    )
  }

  export default IncomeList


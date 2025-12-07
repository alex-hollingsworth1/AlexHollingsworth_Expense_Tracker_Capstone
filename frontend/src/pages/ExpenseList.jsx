import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchExpenses, fetchCategories } from '../services/api'
import FilterBar from '../components/FilterBar'
import '../Transactions.css'

function ExpenseList() {

  const [expenses, setExpenses] = useState([])
  const [categories, setCategories] = useState([])

  // Filter state
  const [filters, setFilters] = useState({
    category: '',        // or 'all' for "All Categories"
    dateFrom: '',
    dateTo: '',
    amountMin: '',
    amountMax: '',
    searchText: '',      // for note/name search
    sortBy: 'date',      // default sort
    sortOrder: 'desc'    // 'asc' or 'desc'
  })

  // Original data (from API)
  const [allExpenses, setAllExpenses] = useState([])

  // Filtered/displayed data
  const [filteredExpenses, setFilteredExpenses] = useState([])

  useEffect(() => {
    fetchExpenses()
      .then(setExpenses)
      .catch(console.error)
    
    fetchCategories()
      .then(setCategories)
      .catch(console.error)
  }, [])

  // Handler that updates filters state
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  return (
    <section className="section-listing">
      <h1>Expenses</h1>
      
      <FilterBar 
        filters={filters}
        onFilterChange={handleFilterChange}
        categories={categories}
      />
      
      {expenses.length > 0 ? (
        <ul>
          {expenses.map((expense) => (
            <li key={expense.id}>
              <Link to={`/expenses/${expense.id}`}>
                <article>
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

export default ExpenseList


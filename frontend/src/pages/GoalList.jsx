import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchGoals } from '../services/api'
import '../Transactions.css'

function GoalList() {
  // Filter state
  const [filters, setFilters] = useState({
    targetMin: '',
    deadlineBy: '',
    searchText: '',
    status: ''
  })

  // Original data (from API)
  const [allGoals, setAllGoals] = useState([])

  // Filtered/displayed data
  const [filteredGoals, setFilteredGoals] = useState([])

  useEffect(() => {
    fetchGoals()
      .then(setAllGoals)
      .catch(console.error)
  }, [])

  useEffect(() => {
    applyFilters()
  }, [allGoals, filters])

  // Handler that updates filters state
  const handleFilterChange = (field, value) => {
    setFilters({
      ...filters,
      [field]: value
    })
  }

  const applyFilters = () => {
    let filtered = [...allGoals]

    // Filter by min target
    if (filters.targetMin) {
      filtered = filtered.filter((goal) => {
        return parseFloat(goal.target) >= parseFloat(filters.targetMin)
      })
    }

    // Filter by deadline (deadline by)
    if (filters.deadlineBy) {
      filtered = filtered.filter((goal) => {
        return goal.deadline <= filters.deadlineBy
      })
    }

    // Filter by note (search text)
    if (filters.searchText) {
      filtered = filtered.filter((goal) => {
        return goal.note?.toLowerCase().includes(filters.searchText.toLowerCase())
      })
    }

    // Filter by status
    if (filters.status && filters.status !== 'all') {
      filtered = filtered.filter((goal) => {
        return goal.status === filters.status
      })
    }

    setFilteredGoals(filtered)
  }

  return (
    <section className="section-listing">
      <h1>Goals</h1>

      {/* Custom Filter Bar for Goals */}
      <div className="filter-bar">
        {/* Min Target */}
        <div className="filter-slot">
          <label>Min Target</label>
          <input
            type="number"
            value={filters.targetMin}
            onChange={(e) => handleFilterChange('targetMin', e.target.value)}
          />
        </div>

        {/* Deadline By */}
        <div className="filter-slot">
          <label>Deadline By</label>
          <input
            type="date"
            value={filters.deadlineBy}
            onChange={(e) => handleFilterChange('deadlineBy', e.target.value)}
          />
        </div>

        {/* Search Notes */}
        <div className="filter-slot">
          <label>Search Notes</label>
          <input
            type="text"
            value={filters.searchText}
            onChange={(e) => handleFilterChange('searchText', e.target.value)}
          />
        </div>

        {/* Status */}
        <div className="filter-slot">
          <label>Status</label>
          <select
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="Not Started">Not Started</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
      </div>

      {filteredGoals.length > 0 ? (
        <ul>
          {filteredGoals.map((goal) => (
            <li key={goal.id}>
              <Link to={`/goals/${goal.id}`}>
                <article>
                  <h2>{goal.name}</h2>
                  <p className="meta">
                    <strong>Target:</strong> ${goal.target} · <strong>Deadline:</strong> {goal.deadline} · <strong>Status:</strong> {goal.status}
                  </p>
                </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No goals yet.</p>
      )}
    </section>
  )
}

export default GoalList


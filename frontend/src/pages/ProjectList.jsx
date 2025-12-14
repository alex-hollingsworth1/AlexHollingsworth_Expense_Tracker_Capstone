import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchProjects, fetchClients } from '../services/api'
import FilterBar from '../components/FilterBar'
import '../Transactions.css'

function ProjectList() {

  // Filter state
  const [filters, setFilters] = useState({
    client: '',
    name: '',
    dateCreated: '',
    searchText: '',
    sortBy: 'dateCreated',
    sortOrder: 'desc'
  })

  // Original data (from API)
  const [allProjects, setAllProjects] = useState([])
  const [clients, setClients] = useState([])

  // Filtered/displayed data
  const [filteredProjects, setFilteredProjects] = useState([])

  useEffect(() => {
    fetchProjects()
      .then(setAllProjects)
      .catch(console.error)
    
    fetchClients()
      .then(setClients)
      .catch(console.error)
  }, [])

  useEffect(() => {
    applyFilters()
  }, [allProjects, filters])

  // Handler that updates filters state
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  const applyFilters = () => {
    let filtered = [...allProjects]

    if (filters.client && filters.client !== 'all') {
      filtered = filtered.filter((project) => {
        return project.client?.id === parseInt(filters.client)
      })
    }

    if (filters.dateCreated) {
      filtered = filtered.filter((project) => {
        return project.date_created >= filters.dateCreated
      })
    }

    if (filters.searchText) {
      filtered = filtered.filter((project) => {
        const searchLower = filters.searchText.toLowerCase()
        return project.name?.toLowerCase().includes(searchLower) ||
               project.note?.toLowerCase().includes(searchLower)
      })
    }

    if (filters.sortBy == 'client') {
        filtered.sort((a, b) => {
          const clientA = (a.client?.name || '').toLowerCase()
          const clientB = (b.client?.name || '').toLowerCase()
          const comparison = clientA.localeCompare(clientB)
          return filters.sortOrder === 'desc' ? -comparison : comparison
        })
      }

    if (filters.sortBy == 'name') {
      filtered.sort((a, b) => {
        const nameA = (a.name || '').toLowerCase()
        const nameB = (b.name || '').toLowerCase()
        const comparison = nameA.localeCompare(nameB)
        return filters.sortOrder === 'desc' ? -comparison : comparison
      })
    }


    if (filters.sortBy == 'dateCreated') {
      filtered.sort((a, b) => {
        const dateA = new Date(a.date_created)
        const dateB = new Date(b.date_created)
        const comparison = dateA - dateB
        return filters.sortOrder === 'desc' ? -comparison : comparison
      })
    }

    setFilteredProjects(filtered)
  }


  return (
    <section className="section-listing">
      <h1>Projects</h1>

      <FilterBar
        filters={filters}
        onFilterChange={handleFilterChange}
        categories={null}
        clients={clients}
      />

      {filteredProjects.length > 0 ? (
        <ul>
          {filteredProjects.map((project) => (
            <li key={project.id}>
              <Link to={`/projects/${project.id}`}>
                <article className="project-item">
                  <h2>{project.name}</h2>
                  <p>{project.note || 'No note provided.'}</p>
                </article>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No projects yet.</p>
      )}
    </section>
  )
}

export default ProjectList;


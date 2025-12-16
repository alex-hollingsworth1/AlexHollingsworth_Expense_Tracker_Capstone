import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchClients } from '../services/api'
import FilterBar from '../components/FilterBar'
import '../styles/Transactions.css'

function ClientList() {

    // Filter state
    const [filters, setFilters] = useState({
        name: '',
        email: '',
        phone_number: '',
        sortBy: 'name',
        sortOrder: 'desc'
    })

    // Original data (from API)
    const [allClients, setAllClients] = useState([])
    //   const [clients, setClients] = useState([])

    // Filtered/displayed data
    const [filteredClients, setFilteredClients] = useState([])

    useEffect(() => {

        fetchClients()
            .then(setAllClients)
            .catch(console.error)
    }, [])

    useEffect(() => {
        applyFilters()
    }, [allClients, filters])

    // Handler that updates filters state
    const handleFilterChange = (newFilters) => {
        setFilters(newFilters)
    }

    const applyFilters = () => {
        let filtered = [...allClients]

        if (filters.name && filters.name.trim() !== 'all') {
            filtered = filtered.filter((client) => {
                return client.name?.toLowerCase().includes(filters.name.toLowerCase())
            })
        }

        if (filters.email && filters.email.trim() !== '') {
            filtered = filtered.filter((client) => {
                return client.email?.toLowerCase().includes(filters.email.toLowerCase())
            })
        }

        if (filters.phone_number && filters.phone_number.trim() !== '') {
            filtered = filtered.filter((client) => {
                return client.phone_number?.toLowerCase().includes(filters.phone_number.toLowerCase())
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

        setFilteredClients(filtered)
    }

    return (
        <section className="section-listing">
            <h1>Clients</h1>

            <FilterBar
                filters={filters}
                onFilterChange={handleFilterChange}
                categories={null}
                clients={null}
            />

            {filteredClients.length > 0 ? (
                < ul >
            {
                filteredClients.map((client) => (
                    < li key = { client.id } >
                    <Link to={`/clients/${client.id}`}>
                        <article className="client-item">
                            <h2>{client.name}</h2>
                            <p className="meta">
                                <strong>Email:</strong> {client.email} · <strong>Phone:</strong> {client.phone_number || 'No phone provided.'}
                            </p>
                        </article>
                    </Link>
                </li>
                ))
            }
            </ul >
          ) : (
            <p>No clients yet.</p>
        )}
        </section >
      )
    }

export default ClientList;


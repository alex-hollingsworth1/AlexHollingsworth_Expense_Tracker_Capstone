import { useAuth } from '../contexts/AuthContext'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

function RedirectIfAuthenticated({children}) {
    const {isAuthenticated, loading } = useAuth()
    const navigate = useNavigate()

    useEffect(() => {
        if (!loading && isAuthenticated) {
            navigate('/dashboard')
        }
    }, [isAuthenticated, loading, navigate])

    if (loading) return null;
    return children;
}

export default RedirectIfAuthenticated;
import { createContext, useContext, useState, useEffect } from 'react'
import { loginUser } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const token = localStorage.getItem('access_token')
        
        if (token) {
          setIsAuthenticated(true)
        } else {
          setIsAuthenticated(false)
        }
        
        setLoading(false)
      }, [])

      const login = async (username, password) => {
        try {
          await loginUser(username, password)
          setIsAuthenticated(true)
          return { success: true }
        } catch (error) {
          setIsAuthenticated(false)
          return { success: false, error: error.message }
        }
      }

      const logout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        setIsAuthenticated(false)
        setUser(null)
      }

      const value = {
        isAuthenticated,
        user,
        loading,
        login,
        logout,
      }

      return (
        <AuthContext.Provider value={value}>
          {children}
        </AuthContext.Provider>
      )
      
}

export function useAuth() {
    const context = useContext(AuthContext)
    
    if (!context) {
      throw new Error('useAuth must be used within an AuthProvider')
    }
    
    return context
  }
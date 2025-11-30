import { useAuth } from "../contexts/AuthContext";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function ProtectedRoute({children}) {
    const {isAuthenticated, loading } = useAuth()
    const navigate = useNavigate()

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            navigate("/")
        }
    }, [isAuthenticated, loading, navigate])

    if (loading) return null;
    if (!isAuthenticated) return null;
    return children;

}

export default ProtectedRoute;
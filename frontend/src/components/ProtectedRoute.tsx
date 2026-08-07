import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from '../context/AuthContext';

export const ProtectedRoute = () => {
const { isAuthenticated, loading } = useAuth();

    if (loading) {
        return (
        <div className="min-h-screen bg-frio flex items-center justify-center text-texto-suave">
            Verificando sesión...
        </div>
        );
    }

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

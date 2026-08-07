import type { ReactNode } from 'react';
import { createContext, useContext, useState, useEffect } from 'react';
import { apiDjango } from '../api/cliente';
import type { Usuario } from '../types';

interface AuthContextType {
    isAuthenticated: boolean;
    user: Usuario | null;
    login: (userData: Usuario) => void;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState<Usuario | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const verificarSesion = async () => {
            try {
                const response = await apiDjango.get('/me/');
                setIsAuthenticated(true);
                setUser(response.data);
            } catch {
                setIsAuthenticated(false);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };
        verificarSesion();
    }, []);

    const login = (userData: Usuario) => {
        setIsAuthenticated(true);
        setUser(userData);
    };

    const logout = () => {
        setIsAuthenticated(false);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth debe usarse dentro de AuthProvider');
    return context;
};

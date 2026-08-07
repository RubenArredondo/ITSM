import { useNavigate } from "react-router-dom";
import { apiDjango } from "../../api/cliente";
import { useAuth } from "../../context/AuthContext";

export default function BotonLogout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await apiDjango.post("/logout/");
    } finally {
      logout();
      navigate("/login");
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="rounded border border-fondo/40 px-3 py-1 text-sm text-fondo transition-colors hover:bg-fondo/10"
    >
      Cerrar sesión
    </button>
  );
}

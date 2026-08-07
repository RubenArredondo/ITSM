import { useState, type SyntheticEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { apiDjango } from "../api/cliente";

export default function Registro() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const navigate = useNavigate();

  const handleRegistro = async (e: SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setEnviando(true);

    try {
      await apiDjango.post("/register/", { username, email, password });
      navigate("/login");
    } catch {
      setError(
        "No se pudo crear la cuenta. Revisa los datos e intenta de nuevo.",
      );
    } finally {
      setEnviando(false);
    }
  };

  return (
    <div className="min-h-screen bg-frio flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-fondo rounded-lg shadow-sm border border-borde p-8">
        <h1 className="text-2xl font-bold text-cerceta mb-1">Crear cuenta</h1>
        <p className="text-texto-suave text-sm mb-6">
          Regístrate para reportar incidentes
        </p>

        {error && (
          <div className="mb-4 rounded border-l-4 border-alerta bg-alerta/10 px-4 py-3 text-sm text-alerta">
            {error}
          </div>
        )}

        <form onSubmit={handleRegistro} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-texto mb-1">
              Usuario
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded border border-borde px-3 py-2 text-texto outline-none focus:border-cerceta"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-texto mb-1">
              Correo
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded border border-borde px-3 py-2 text-texto outline-none focus:border-cerceta"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-texto mb-1">
              Contraseña
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded border border-borde px-3 py-2 text-texto outline-none focus:border-cerceta"
              required
            />
          </div>

          <button
            type="submit"
            disabled={enviando}
            className="w-full rounded bg-cerceta py-2 font-semibold text-fondo transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {enviando ? "Creando cuenta..." : "Crear cuenta"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-texto-suave">
          ¿Ya tienes cuenta?{" "}
          <Link
            to="/login"
            className="text-cerceta font-medium hover:underline"
          >
            Inicia sesión
          </Link>
        </p>
      </div>
    </div>
  );
}

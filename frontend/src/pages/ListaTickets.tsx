import { useAuth } from '../context/AuthContext';
import BotonLogout from "../components/botones/BotonLogout";

export default function ListaTickets() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-frio">
      <header className="bg-cerceta text-fondo px-6 h-15 flex items-center justify-between">
        <h1 className="text-xl font-semibold">Centro de Soporte Técnico</h1>
        <div className="flex items-center gap-4 text-sm">
          <span>{user?.username} ({user?.rol})</span>
          <BotonLogout />
        </div>
      </header>

      <main className="p-8">
        <p className="text-texto">Aquí va la tabla de tickets.</p>
      </main>
    </div>
  );
}

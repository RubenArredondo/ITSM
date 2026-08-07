import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import BotonLogout from "../components/botones/BotonLogout";

export default function DashboardLayout() {
  const { user } = useAuth();

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-frio">
      <header className="h-15 shrink-0 z-10 flex items-center justify-between bg-cerceta px-6 text-fondo shadow-sm">
        <h1 className="text-xl font-semibold">Centro de Soporte Técnico</h1>

        <div className="flex items-center gap-4 text-sm">
          <span>
            {user?.username} ({user?.rol})
          </span>
          <BotonLogout />
        </div>
      </header>

      <main className="flex flex-1 min-h-0 flex-col p-6">
        <Outlet />
      </main>
    </div>
  );
}

import { useEffect, useState } from "react";
import { apiDjango } from "../api/cliente";
import { useAuth } from "../context/AuthContext";
import { CapsulaPrioridad, CapsulaEstado } from "../components/Capsulas";
import CeldaSla from "../components/CeldaSla";
import type { Ticket } from "../types";

type Filtro = "todos" | "mios" | "urgentes";

export default function ListaTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filtro, setFiltro] = useState<Filtro>("todos");

  const { user } = useAuth();

  useEffect(() => {
    const traerTickets = async () => {
      setCargando(true);
      setError(null);

      const ruta = filtro === "urgentes" ? "/tickets/urgencias/" : "/tickets/";

      try {
        const respuesta = await apiDjango.get(ruta);
        setTickets(respuesta.data);
      } catch {
        setError("No se pudieron cargar los tickets.");
      } finally {
        setCargando(false);
      }
    };

    traerTickets();
  }, [filtro]);

  const visibles =
    filtro === "mios"
      ? tickets.filter((t) => t.solicitante === user?.id)
      : tickets;

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="mb-4 flex gap-3">
        <BotonFiltro activo={filtro === "todos"} onClick={() => setFiltro("todos")}>
          Todos los Tickets
        </BotonFiltro>

        <BotonFiltro activo={filtro === "mios"} onClick={() => setFiltro("mios")}>
          Solo mis tickets
        </BotonFiltro>

        <BotonFiltro
          activo={filtro === "urgentes"}
          onClick={() => setFiltro("urgentes")}
          urgente
        >
          Urgentes (SLA &lt; 2h)
        </BotonFiltro>
      </div>

      {cargando && <p className="text-texto-suave">Cargando tickets...</p>}

      {error && (
        <div className="rounded border-l-4 border-alerta bg-alerta/10 px-4 py-3 text-sm text-alerta">
          {error}
        </div>
      )}

      {!cargando && !error && (
        <div className="min-h-0 flex-1 overflow-y-auto rounded-lg border border-borde bg-fondo shadow-sm">
          <table className="w-full text-left">
            <thead className="sticky top-0 z-1 bg-frio">
              <tr>
                {["ID", "Asunto", "Solicitante", "Prioridad", "Estado", "SLA"].map((titulo) => (
                  <th
                    key={titulo}
                    className="px-4 py-3 text-xs font-semibold uppercase text-texto-suave"
                  >
                    {titulo}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {visibles.map((ticket) => (
                <tr
                  key={ticket.id}
                  className="cursor-pointer border-b border-borde transition-colors hover:bg-frio"
                >
                  <td className="px-4 py-3 text-texto">#{ticket.id}</td>
                  <td className="px-4 py-3 text-texto">{ticket.titulo}</td>
                  <td className="px-4 py-3 text-texto">{ticket.solicitante_username}</td>
                  <td className="px-4 py-3">
                    <CapsulaPrioridad prioridad={ticket.prioridad} />
                  </td>
                  <td className="px-4 py-3">
                    <CapsulaEstado estado={ticket.estado} />
                  </td>
                  <td className="px-4 py-3">
                    <CeldaSla fecha={ticket.fecha_vencimiento_sla} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {visibles.length === 0 && (
            <p className="p-8 text-center text-texto-suave">
              No hay tickets para mostrar.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function BotonFiltro({
  activo,
  urgente,
  onClick,
  children,
}: {
  activo: boolean;
  urgente?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  const base = "rounded-md border px-4 py-2 text-sm font-medium transition-colors";

  if (activo) {
    return (
      <button
        onClick={onClick}
        className={`${base} ${urgente ? "border-alerta bg-alerta text-fondo" : "border-cerceta bg-cerceta text-fondo"}`}
      >
        {children}
      </button>
    );
  }

  return (
    <button
      onClick={onClick}
      className={`${base} bg-fondo hover:bg-borde ${urgente ? "border-alerta text-alerta" : "border-borde text-texto"}`}
    >
      {children}
    </button>
  );
}

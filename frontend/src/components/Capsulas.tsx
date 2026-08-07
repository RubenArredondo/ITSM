import type { Prioridad, Estado } from "../types";

type Color = "alerta" | "precaucion" | "cerceta" | "suave";

const CLASES: Record<Color, string> = {
  alerta: "bg-alerta",
  precaucion: "bg-precaucion",
  cerceta: "bg-cerceta",
  suave: "bg-texto-suave",
};

function Capsula({ texto, color }: { texto: string; color: Color }) {
  return (
    <span
      className={`inline-block rounded-md px-3 py-1 text-xs font-semibold text-fondo ${CLASES[color]}`}
    >
      {texto}
    </span>
  );
}

const COLOR_PRIORIDAD: Record<Prioridad, Color> = {
  CRITICA: "alerta",
  ALTA: "precaucion",
  MEDIA: "cerceta",
  BAJA: "cerceta",
};

export function CapsulaPrioridad({ prioridad }: { prioridad: Prioridad }) {
  return <Capsula texto={prioridad} color={COLOR_PRIORIDAD[prioridad]} />;
}

const COLOR_ESTADO: Record<Estado, Color> = {
  NUEVO: "cerceta",
  EN_REVISION: "precaucion",
  ESPERANDO_CLIENTE: "precaucion",
  RESUELTO: "suave",
  CERRADO: "suave",
};

export function CapsulaEstado({ estado }: { estado: Estado }) {
  return <Capsula texto={estado.replace("_", " ")} color={COLOR_ESTADO[estado]} />;
}

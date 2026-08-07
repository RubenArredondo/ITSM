export default function CeldaSla({ fecha }: { fecha: string | null }) {
  if (!fecha) {
    return <span className="text-texto-suave">—</span>;
  }

  const minutos = Math.round(
    (new Date(fecha).getTime() - new Date().getTime()) / 60000,
  );

  if (minutos < 0) {
    return <span className="font-bold text-alerta">Vencido</span>;
  }

  const urgente = minutos < 120;

  let texto: string;
  if (minutos < 60) {
    texto = `${minutos} min restantes`;
  } else if (minutos < 1440) {
    texto = `${Math.floor(minutos / 60)} h restantes`;
  } else {
    texto = `${Math.floor(minutos / 1440)} días restantes`;
  }

  return (
    <span className={urgente ? "font-bold text-alerta" : "text-texto"}>
      {texto}
    </span>
  );
}

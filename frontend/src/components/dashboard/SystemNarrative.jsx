export default function SystemNarrative() {
  return (
    <aside className="min-w-0 rounded-xl bg-[#003049] p-6 text-[#fdf0d5] shadow-sm">
      <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#669bbc]">
        System narrative
      </p>
      <h2 className="mt-2 text-xl font-bold">
        Una operación que se explica sola.
      </h2>
      <p className="mt-3 text-sm leading-6 text-white/70">
        NEXUS convierte cada señal biométrica en una lectura operacional clara,
        desde la entrada hasta el cierre de jornada.
      </p>
      <div className="mt-6 space-y-3">
        {["Captura biométrica", "Normalización de eventos", "Lectura operativa"].map(
          (step, index) => (
            <div key={step} className="flex items-center gap-3 text-sm font-semibold">
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#c1121f] text-xs">
                0{index + 1}
              </span>
              <span>{step}</span>
            </div>
          ),
        )}
      </div>
    </aside>
  );
}

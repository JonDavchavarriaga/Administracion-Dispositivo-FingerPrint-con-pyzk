function statusCopy(status) {
  if (status === "error") return { label: "Desconectado", tone: "critical" };
  if (status === "connecting") return { label: "Conectando", tone: "pending" };
  if (status === "connected" || status === "healthy") {
    return { label: "En línea", tone: "online" };
  }
  return { label: "Sin estado", tone: "neutral" };
}

const tones = {
  online: "bg-emerald-50 text-emerald-700",
  critical: "bg-red-50 text-[#780000]",
  pending: "bg-amber-50 text-amber-700",
  neutral: "bg-slate-100 text-slate-600",
};

export default function DeviceObservatory({ devices, syncing, onSync }) {
  return (
    <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
      {devices.map((device) => {
        const state = statusCopy(device.status);
        const deviceId = device.device_id ?? device.id;
        return (
          <article
            key={deviceId}
            className="rounded-xl border border-[#669bbc]/20 bg-white p-5 shadow-sm"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0">
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#669bbc]">
                  Punto 0{deviceId}
                </p>
                <h3 className="mt-2 truncate text-lg font-bold text-[#003049]">
                  {device.name}
                </h3>
                <p className="mt-1 truncate text-xs text-slate-500">{device.ip}</p>
              </div>
              <span className={`flex shrink-0 items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${tones[state.tone]}`}>
                <span className={`h-2 w-2 rounded-full ${
                  state.tone === "online"
                    ? "animate-pulse bg-emerald-500"
                    : state.tone === "critical"
                      ? "bg-[#c1121f]"
                      : "bg-[#669bbc]"
                }`} />
                {state.label}
              </span>
            </div>
            <div className="mt-6 flex items-center justify-between border-t border-slate-100 pt-4">
              <span className="text-xs text-slate-500">Intervalo: {device.interval_seconds}s</span>
              <button
                type="button"
                onClick={() => onSync(deviceId)}
                disabled={syncing !== null}
                className="rounded-lg bg-[#c1121f] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#780000] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {syncing === deviceId ? "Procesando…" : "Sincronizar"}
              </button>
            </div>
          </article>
        );
      })}
    </section>
  );
}

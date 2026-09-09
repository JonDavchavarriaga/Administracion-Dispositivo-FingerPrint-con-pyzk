const deviceNames = {
  1: "Entrada principal",
  2: "Comedor corporativo",
  3: "Salida principal",
};

function formatTime(value) {
  return new Date(value).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function ActivityStream({ records, loading }) {
  return (
    <section className="min-w-0 rounded-xl border border-[#669bbc]/20 bg-white shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 px-6 py-5">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#780000]">
            Activity stream
          </p>
          <h2 className="mt-1 text-xl font-bold text-[#003049]">
            Últimas marcaciones
          </h2>
        </div>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
          Telemetría activa
        </span>
      </div>

      <div className="max-h-[400px] overflow-y-auto">
        {loading ? (
          <p className="p-8 text-sm text-slate-500">Cargando señales…</p>
        ) : records.length === 0 ? (
          <p className="p-8 text-sm text-slate-500">
            Ejecuta una sincronización para iniciar la demo.
          </p>
        ) : (
          <div className="divide-y divide-slate-100">
            {records.map((record, index) => (
              <div
                key={`${record.device_id}-${record.timestamp}-${index}`}
                className="flex items-center gap-4 px-6 py-4"
              >
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#fdf0d5] font-bold text-[#780000]">
                  {record.device_id === 2 ? "C" : record.device_id === 3 ? "S" : "E"}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold text-[#003049]">
                    Cédula {record.user_external_id || record.user_id}
                  </p>
                  <p className="truncate text-xs text-slate-500">
                    {deviceNames[record.device_id] || `Dispositivo ${record.device_id}`}
                  </p>
                </div>
                <time className="shrink-0 text-sm font-semibold text-slate-500">
                  {formatTime(record.timestamp)}
                </time>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

import { useEffect, useMemo, useState } from "react";
import { getAttendance } from "../api/attendance.api";
import { useDeviceStatus } from "../hooks/useDeviceStatus";

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

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [liveStatus, setLiveStatus] = useState("connected");

  async function loadAttendance() {
    try {
      const data = await getAttendance();
      setRecords(Array.isArray(data) ? data : []);
      setLastUpdate(new Date());
    } catch (error) {
      console.error("Error loading attendance:", error);
    } finally {
      setLoading(false);
    }
  }

  useDeviceStatus((event) => {
    if (event.type === "device_status_changed") {
      setLiveStatus(event.status === "error" ? "attention" : "connected");
      if (event.status === "healthy") loadAttendance();
    }
  });

  useEffect(() => {
    loadAttendance();
  }, []);

  const uniqueUsers = useMemo(
    () => new Set(records.map((record) => record.user_external_id || record.user_id)).size,
    [records],
  );
  const recentRecords = records.slice(-8).reverse();
  const deviceCount = new Set(records.map((record) => record.device_id)).size;

  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-[2rem] bg-[#003049] px-8 py-9 text-[#fdf0d5] shadow-xl shadow-[#003049]/10">
        <div className="absolute -right-20 -top-24 h-72 w-72 rounded-full border-[34px] border-[#c1121f]/30" />
        <div className="absolute right-24 -bottom-28 h-56 w-56 rounded-full border-[20px] border-[#669bbc]/20" />
        <div className="relative max-w-2xl">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#669bbc]">
            Live workforce intelligence
          </p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight md:text-4xl">
            Visibilidad operativa, sin puntos ciegos.
          </h2>
          <p className="mt-4 max-w-xl text-sm leading-6 text-white/70">
            NEXUS consolida las señales de tu red biométrica y convierte cada
            marcación en una lectura clara de la operación.
          </p>
          <div className="mt-6 flex items-center gap-3 text-sm">
            <span className={`h-2.5 w-2.5 rounded-full ${
              liveStatus === "attention" ? "bg-[#c1121f]" : "bg-emerald-400"
            } animate-pulse`} />
            {liveStatus === "attention" ? "Requiere atención" : "Telemetría en vivo"}
            <span className="text-white/40">·</span>
            Actualizado {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {[
          ["Marcaciones procesadas", records.length, "Eventos recibidos"],
          ["Personas identificadas", uniqueUsers, "Cédulas únicas"],
          ["Puntos activos", deviceCount || 3, "Entrada · Comedor · Salida"],
        ].map(([label, value, caption], index) => (
          <div key={label} className="rounded-2xl border border-[#003049]/10 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between">
              <p className="text-sm font-medium text-slate-500">{label}</p>
              <span className={`rounded-lg px-2 py-1 text-xs font-bold ${
                index === 1 ? "bg-[#fdf0d5] text-[#780000]" : "bg-[#e8f3f6] text-[#003049]"
              }`}>
                5m
              </span>
            </div>
            <p className="mt-3 text-3xl font-bold text-[#003049]">{value}</p>
            <p className="mt-1 text-xs text-slate-400">{caption}</p>
          </div>
        ))}
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="rounded-2xl border border-[#003049]/10 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 px-6 py-5">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#780000]">
                Activity stream
              </p>
              <h3 className="mt-1 text-lg font-bold text-[#003049]">Últimas marcaciones</h3>
            </div>
            <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
              En vivo
            </span>
          </div>
          {loading ? (
            <div className="p-8 text-sm text-slate-400">Cargando señales…</div>
          ) : recentRecords.length === 0 ? (
            <div className="p-8 text-sm text-slate-400">Ejecuta una sincronización para iniciar la demo.</div>
          ) : (
            <div className="divide-y divide-slate-100">
              {recentRecords.map((record, index) => (
                <div key={`${record.device_id}-${record.timestamp}-${index}`} className="flex items-center gap-4 px-6 py-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#fdf0d5] text-[#780000]">
                    {record.device_id === 2 ? "⌁" : record.device_id === 3 ? "↗" : "↘"}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold text-[#003049]">
                      Cédula {record.user_external_id || record.user_id}
                    </p>
                    <p className="text-xs text-slate-400">
                      {deviceNames[record.device_id] || `Dispositivo ${record.device_id}`}
                    </p>
                  </div>
                  <time className="text-sm font-semibold text-slate-500">{formatTime(record.timestamp)}</time>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-2xl bg-[#fdf0d5] p-6">
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#780000]">System narrative</p>
          <h3 className="mt-2 text-xl font-bold text-[#003049]">Una operación que se explica sola.</h3>
          <p className="mt-3 text-sm leading-6 text-[#003049]/70">
            La demo simula la hora pico: personas que entran, pasan por el
            comedor y registran su salida. Cada evento atraviesa el mismo
            pipeline que usaría una instalación real.
          </p>
          <div className="mt-6 space-y-3">
            {["Captura biométrica", "Normalización de eventos", "Lectura operativa"].map((step, index) => (
              <div key={step} className="flex items-center gap-3 text-sm font-semibold text-[#003049]">
                <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#003049] text-xs text-[#fdf0d5]">
                  0{index + 1}
                </span>
                {step}
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

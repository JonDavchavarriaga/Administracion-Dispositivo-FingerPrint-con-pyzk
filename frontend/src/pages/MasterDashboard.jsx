import { useEffect, useMemo, useState } from "react";
import { getAttendance } from "../api/attendance.api";
import { getDevices, syncAllDevices, syncDevice } from "../api/devices.api";
import { useDeviceStatus } from "../hooks/useDeviceStatus";

const deviceLabels = {
  1: "Entrada principal",
  2: "Comedor corporativo",
  3: "Salida principal",
};

function statusInfo(status) {
  if (status === "error") return { label: "Desconectado", className: "bg-red-100 text-red-800", dot: "bg-[#c1121f]" };
  if (status === "connecting") return { label: "Conectando", className: "bg-amber-100 text-amber-800", dot: "bg-amber-500" };
  return { label: "En línea", className: "bg-green-100 text-green-800", dot: "bg-green-500" };
}

function formatTime(value) {
  return new Date(value).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function Metric({ label, value, caption }) {
  return (
    <article className="flex aspect-square min-h-44 flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white p-5 text-center shadow-md transition hover:-translate-y-1 hover:shadow-lg">
      <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-[#669bbc]">{label}</p>
      <p className="mt-3 text-4xl font-bold text-[#003049] sm:text-5xl">{value}</p>
      <p className="mt-2 max-w-[13rem] text-xs leading-5 text-slate-500">{caption}</p>
    </article>
  );
}

function ActivityStream({ records, loading }) {
  return (
    <section className="min-w-0 rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-gray-200 px-5 py-5 sm:px-6">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#669bbc]">Telemetría en vivo</p>
          <h2 className="mt-1 text-xl font-bold text-[#003049]">Últimas marcaciones</h2>
        </div>
        <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-800">Canal activo</span>
      </div>
      <div className="max-h-[400px] overflow-y-auto">
        {loading ? <p className="p-8 text-sm text-slate-500">Cargando actividad...</p> : records.length === 0 ? (
          <p className="p-8 text-sm text-slate-500">Sin marcaciones todavía. Sincroniza un dispositivo para iniciar la demo.</p>
        ) : records.map((record, index) => {
          const point = record.device_id === 2 ? "C" : record.device_id === 3 ? "S" : "E";
          return (
            <div key={`${record.device_id}-${record.timestamp}-${index}`} style={{ animationDelay: `${Math.min(index, 8) * 90}ms` }} className="animate-stack-in flex items-center justify-between gap-3 border-b border-gray-100 p-4 last:border-b-0 sm:px-6">
              <div className="flex min-w-0 items-center gap-3">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#fdf0d5] font-bold text-[#780000]">{point}</span>
                <div className="min-w-0">
                  <p className="truncate text-sm font-semibold text-[#003049]">Cédula {record.user_external_id || record.user_id}</p>
                  <p className="truncate text-xs text-slate-500">{deviceLabels[record.device_id] || `Dispositivo ${record.device_id}`}</p>
                </div>
              </div>
              <time className="shrink-0 text-xs font-semibold text-slate-500 sm:text-sm">{formatTime(record.timestamp)}</time>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function Narrative() {
  const [open, setOpen] = useState(false);

  return (
    <aside className="relative min-w-0 overflow-hidden rounded-2xl bg-[#003049] p-6 text-white shadow-lg">
      <button type="button" onClick={() => setOpen((value) => !value)} aria-expanded={open} className="group flex w-full items-center gap-4 rounded-xl border border-white/15 bg-white/5 p-3 text-left transition hover:bg-white/10">
        <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[#c1121f] text-2xl font-bold shadow-md transition group-hover:scale-105">?</span>
        <span>
          <span className="block text-xs font-bold uppercase tracking-[0.16em] text-[#669bbc]">¿Cómo funciona?</span>
          <span className="mt-1 block text-sm font-semibold">Conoce el flujo de NEXUS</span>
        </span>
      </button>
      {open && <div className="animate-stack-in mt-5 border-t border-white/10 pt-5">
        <p className="text-sm leading-6 text-white/75">NEXUS recibe las marcaciones de cada punto biométrico, las normaliza y las convierte en una lectura clara de la operación.</p>
        <div className="mt-5 space-y-3">
          {["Captura biométrica", "Normalización de eventos", "Lectura operacional"].map((step, index) => (
            <div key={step} className="flex items-center gap-3 text-sm font-semibold"><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#c1121f] text-xs">0{index + 1}</span>{step}</div>
          ))}
        </div>
      </div>}
    </aside>
  );
}

export default function MasterDashboard() {
  const [records, setRecords] = useState([]);
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(null);
  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [attendance, deviceData] = await Promise.all([getAttendance(), getDevices()]);
      setRecords(Array.isArray(attendance) ? attendance : []);
      setDevices(Array.isArray(deviceData) ? deviceData : []);
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      setLoading(false);
    }
  }

  useDeviceStatus((event) => {
    if (event.type === "device_snapshot") setDevices(event.devices);
    if (event.type === "device_status_changed") {
      setDevices((current) => current.map((device) => (device.device_id ?? device.id) === event.device_id ? { ...device, status: event.status } : device));
      if (event.status === "healthy") loadData();
    }
  });

  useEffect(() => { loadData(); }, []);

  const uniqueUsers = useMemo(() => new Set(records.map((record) => record.user_external_id || record.user_id)).size, [records]);

  async function handleSync(deviceId = "all") {
    setSyncing(deviceId);
    setMessage("");
    try {
      const result = deviceId === "all" ? await syncAllDevices() : await syncDevice(deviceId);
      setMessage(result.status === "completed" ? "Sincronización completada correctamente." : "Sincronización enviada a la cola.");
      await loadData();
    } catch (error) {
      console.error("Error synchronizing devices:", error);
      setMessage("No se pudo iniciar la sincronización.");
    } finally {
      setSyncing(null);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
        <header className="border-b border-gray-200 bg-white px-4 py-6 sm:px-6">
          <div className="mx-auto text-center">
            <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#669bbc]">Biometric operations center</p>
            <h1 className="mt-1 text-2xl font-bold tracking-tight text-[#003049] sm:text-3xl">NEXUS Workforce Intelligence</h1>
          </div>
          <div className="mt-3 flex justify-center"><span className="flex items-center gap-2 rounded-full bg-[#fdf0d5] px-3 py-2 text-xs font-semibold text-[#780000]"><span className="h-2 w-2 animate-pulse rounded-full bg-green-500" />Demo en vivo · MOCK_MODE</span></div>
        </header>

        <main className="mx-auto max-w-7xl space-y-10 p-4 sm:p-6 lg:p-10">
          <div className="flex justify-center">
            <button type="button" onClick={() => handleSync()} disabled={syncing !== null} className="inline-flex items-center gap-2 rounded-xl bg-[#003049] px-5 py-3 text-sm font-bold text-white shadow-md transition hover:-translate-y-0.5 hover:bg-[#669bbc] hover:shadow-lg active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50">{syncing === "all" ? "Sincronizando..." : "↻  Sincronizar toda la red"}</button>
          </div>

          <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <Metric label="Marcaciones procesadas" value={records.length} caption="Eventos recibidos por la plataforma" />
            <Metric label="Personas identificadas" value={uniqueUsers} caption="Cédulas únicas en la operación" />
            <Metric label="Dispositivos activos" value={devices.filter((device) => device.status !== "error").length} caption={`${devices.length} puntos registrados en la red`} />
          </section>

          {message && <div className="rounded-lg border border-[#669bbc]/30 bg-[#fdf0d5] px-4 py-3 text-sm font-medium text-[#780000]">{message}</div>}

          <section className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2"><ActivityStream records={[...records].reverse().slice(0, 30)} loading={loading} /></div>
            <Narrative />
          </section>

          <section>
            <div className="mb-6 text-center">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#669bbc]">Infraestructura</p>
              <h2 className="mt-2 text-3xl font-bold tracking-tight text-[#003049] sm:text-4xl">Red biométrica</h2>
              <p className="mx-auto mt-2 max-w-xl text-sm text-slate-500">Puntos de control independientes, visibles y listos para sincronizar.</p>
            </div>
            {loading ? <div className="rounded-xl border border-gray-200 bg-white p-8 text-sm text-slate-500">Cargando dispositivos...</div> : (
              <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
                {devices.map((device) => {
                  const id = device.device_id ?? device.id;
                  const state = statusInfo(device.status);
                  return <article key={id} className="flex min-h-64 flex-col justify-between rounded-2xl border border-gray-200 bg-white p-6 shadow-md transition hover:-translate-y-1 hover:border-[#669bbc] hover:shadow-xl">
                    <div className="flex items-start justify-between gap-3"><div className="min-w-0"><p className="text-xs font-bold uppercase tracking-[0.14em] text-[#669bbc]">Punto 0{id}</p><h3 className="mt-2 truncate text-lg font-bold text-[#003049]">{device.name}</h3><p className="mt-1 truncate text-xs text-slate-500">{device.ip}</p></div><span className={`flex shrink-0 items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${state.className}`}><span className={`h-2 w-2 rounded-full ${state.dot}`} />{state.label}</span></div>
                    <div className="mt-8 flex items-center justify-between border-t border-gray-100 pt-5"><span className="text-xs text-slate-500">Cada {device.interval_seconds}s</span><button type="button" onClick={() => handleSync(id)} disabled={syncing !== null} className="inline-flex items-center gap-1 rounded-lg border border-[#003049] bg-[#003049] px-3 py-2 text-xs font-bold text-white shadow-sm transition hover:bg-[#669bbc] hover:shadow-md active:scale-95 disabled:cursor-not-allowed disabled:opacity-50">{syncing === id ? "Procesando..." : "↻ Sincronizar"}</button></div>
                  </article>;
                })}
              </div>
            )}
          </section>
        </main>
    </div>
  );
}

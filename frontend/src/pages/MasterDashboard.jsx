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

function Sidebar({ open, onClose }) {
  return (
    <>
      {open && <button aria-label="Cerrar menú" onClick={onClose} className="fixed inset-0 z-30 bg-slate-900/40 md:hidden" />}
      <aside className={`${open ? "flex" : "hidden"} fixed inset-y-0 left-0 z-40 w-72 shrink-0 flex-col bg-[#003049] text-white md:sticky md:top-0 md:flex md:h-screen`}>
        <div className="border-b border-white/10 px-6 py-7">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#c1121f] text-xl font-bold">N</div>
            <div>
              <p className="text-lg font-bold tracking-tight">NEXUS</p>
              <p className="text-[10px] uppercase tracking-[0.18em] text-[#669bbc]">Workforce intelligence</p>
            </div>
          </div>
        </div>
        <div className="flex-1 px-6 py-8">
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#669bbc]">Panel de control</p>
          <p className="mt-3 text-sm leading-6 text-white/70">Una vista unificada para entender asistencia, dispositivos y salud operativa.</p>
        </div>
        <div className="border-t border-white/10 px-6 py-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#669bbc] text-sm font-bold text-[#003049]">AD</div>
            <div>
              <p className="text-sm font-semibold">Administrador</p>
              <p className="text-xs text-[#669bbc]">Demo environment</p>
            </div>
          </div>
          <div className="mt-5 flex items-center gap-2 rounded-lg bg-white/10 px-3 py-2 text-xs text-[#fdf0d5]">
            <span className="h-2 w-2 animate-pulse rounded-full bg-green-400" />
            MOCK_MODE activo
          </div>
        </div>
      </aside>
    </>
  );
}

function Metric({ label, value, caption }) {
  return (
    <article className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <p className="text-xs font-bold uppercase tracking-[0.14em] text-[#669bbc]">{label}</p>
      <p className="mt-3 text-4xl font-bold text-[#003049]">{value}</p>
      <p className="mt-2 text-sm text-slate-500">{caption}</p>
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
            <div key={`${record.device_id}-${record.timestamp}-${index}`} className="flex items-center justify-between gap-3 border-b border-gray-100 p-4 last:border-b-0 sm:px-6">
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
  return (
    <aside className="relative min-w-0 rounded-2xl bg-[#003049] p-6 text-white shadow-lg">
      <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#669bbc]">System narrative</p>
      <h2 className="mt-3 text-2xl font-bold leading-tight">La operación, en una sola lectura.</h2>
      <p className="mt-4 text-sm leading-6 text-white/70">NEXUS transforma señales biométricas en contexto operativo para que el equipo actúe antes de que una incidencia crezca.</p>
      <div className="mt-7 space-y-3">
        {["Captura biométrica", "Normalización de eventos", "Lectura operacional"].map((step, index) => (
          <div key={step} className="flex items-center gap-3 text-sm font-semibold">
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#c1121f] text-xs">0{index + 1}</span>
            {step}
          </div>
        ))}
      </div>
    </aside>
  );
}

export default function MasterDashboard() {
  const [records, setRecords] = useState([]);
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(null);
  const [message, setMessage] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

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
    <div className="min-h-screen bg-gray-50 md:flex">
      <Sidebar open={menuOpen} onClose={() => setMenuOpen(false)} />
      <div className="min-w-0 flex-1">
        <header className="sticky top-0 z-20 flex min-h-20 items-center justify-between border-b border-gray-200 bg-white px-4 py-4 sm:px-6 lg:px-8">
          <button type="button" onClick={() => setMenuOpen(true)} className="rounded-lg border border-gray-200 p-2 text-[#003049] md:hidden" aria-label="Abrir menú">☰</button>
          <div className="ml-3 md:ml-0">
            <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#669bbc]">Biometric operations center</p>
            <h1 className="mt-1 text-lg font-bold text-[#003049] sm:text-xl">NEXUS Workforce Intelligence</h1>
          </div>
          <span className="hidden items-center gap-2 rounded-full bg-[#fdf0d5] px-3 py-2 text-xs font-semibold text-[#780000] sm:flex"><span className="h-2 w-2 rounded-full bg-green-500" />Demo en vivo</span>
        </header>

        <main className="space-y-8 p-4 sm:p-6 lg:p-8">
          <section className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#669bbc]">Resumen ejecutivo</p>
              <h2 className="mt-2 text-2xl font-bold text-[#003049] sm:text-3xl">Centro operativo</h2>
              <p className="mt-2 max-w-2xl text-sm text-slate-500">Asistencia, actividad biométrica y salud de infraestructura en una única vista.</p>
            </div>
            <button type="button" onClick={() => handleSync()} disabled={syncing !== null} className="rounded-lg bg-[#003049] px-4 py-2.5 text-sm font-bold text-white transition hover:bg-[#669bbc] disabled:opacity-50">{syncing === "all" ? "Sincronizando..." : "Sincronizar todo"}</button>
          </section>

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
            <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
              <div><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#669bbc]">Infraestructura</p><h2 className="mt-1 text-2xl font-bold text-[#003049]">Red biométrica</h2></div>
              <p className="text-sm text-slate-500">Sincronización individual por punto de control</p>
            </div>
            {loading ? <div className="rounded-xl border border-gray-200 bg-white p-8 text-sm text-slate-500">Cargando dispositivos...</div> : (
              <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
                {devices.map((device) => {
                  const id = device.device_id ?? device.id;
                  const state = statusInfo(device.status);
                  return <article key={id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                    <div className="flex items-start justify-between gap-3"><div className="min-w-0"><p className="text-xs font-bold uppercase tracking-[0.14em] text-[#669bbc]">Punto 0{id}</p><h3 className="mt-2 truncate text-lg font-bold text-[#003049]">{device.name}</h3><p className="mt-1 truncate text-xs text-slate-500">{device.ip}</p></div><span className={`flex shrink-0 items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${state.className}`}><span className={`h-2 w-2 rounded-full ${state.dot}`} />{state.label}</span></div>
                    <div className="mt-6 flex items-center justify-between border-t border-gray-100 pt-4"><span className="text-xs text-slate-500">Cada {device.interval_seconds}s</span><button type="button" onClick={() => handleSync(id)} disabled={syncing !== null} className="rounded-lg bg-[#003049] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#669bbc] disabled:opacity-50">{syncing === id ? "Procesando..." : "Sincronizar"}</button></div>
                  </article>;
                })}
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}

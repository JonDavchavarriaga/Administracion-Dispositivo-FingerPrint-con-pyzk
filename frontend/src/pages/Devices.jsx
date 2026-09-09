import { useEffect, useState } from "react";
import { createDevice, getDevices, syncAllDevices, syncDevice } from "../api/devices.api";
import DeviceObservatory from "../components/devices/DeviceObservatory";
import DashboardHeader from "../components/dashboard/DashboardHeader";
import { useDeviceStatus } from "../hooks/useDeviceStatus";

export default function Devices() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [syncing, setSyncing] = useState(null);
  const [message, setMessage] = useState("");

  useDeviceStatus((event) => {
    if (event.type === "device_snapshot") {
      setDevices(event.devices);
    }
    if (event.type === "device_status_changed") {
      setDevices((current) =>
        current.map((device) =>
          (device.device_id ?? device.id) === event.device_id
            ? { ...device, status: event.status }
            : device,
        ),
      );
    }
  });

  async function loadDevices() {
    try {
      const data = await getDevices();
      setDevices((current) => {
        const statuses = new Map(
          current.map((device) => [device.device_id ?? device.id, device.status]),
        );
        return Array.isArray(data)
          ? data.map((device) => ({
              ...device,
              status: device.status || statuses.get(device.device_id ?? device.id),
            }))
          : [];
      });
    } catch (error) {
      console.error("Error loading devices:", error);
      setDevices([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDevices();
  }, []);

  async function handleSync(deviceId) {
    setSyncing(deviceId);
    setMessage("");
    try {
      const result = await syncDevice(deviceId);
      setMessage(result.status === "completed" ? "Sincronización completada." : "Trabajo enviado a la cola.");
      await loadDevices();
    } catch (error) {
      console.error("Error synchronizing device:", error);
      setMessage("No se pudo iniciar la sincronización.");
    } finally {
      setSyncing(null);
    }
  }

  async function handleSyncAll() {
    setSyncing("all");
    setMessage("");
    try {
      const result = await syncAllDevices();
      setMessage(result.status === "completed" ? "Red sincronizada correctamente." : "Sincronizaciones enviadas a la cola.");
      await loadDevices();
    } catch (error) {
      console.error("Error synchronizing devices:", error);
      setMessage("No se pudo sincronizar la red.");
    } finally {
      setSyncing(null);
    }
  }

  async function handleCreate(device) {
    await createDevice(device);
    setShowForm(false);
    await loadDevices();
  }

  return (
    <div className="space-y-8">
      <DashboardHeader
        eyebrow="Infrastructure observatory"
        title="Red biométrica"
        description="Monitorea los puntos de entrada, comedor y salida desde una única superficie operacional."
        action={
          <>
            <button
              type="button"
              onClick={handleSyncAll}
              disabled={syncing !== null}
              className="rounded-lg bg-[#c1121f] px-4 py-2.5 text-sm font-bold text-white transition hover:bg-[#780000] disabled:opacity-50"
            >
              {syncing === "all" ? "Sincronizando…" : "Sincronizar todo"}
            </button>
            <button
              type="button"
              onClick={() => setShowForm(true)}
              className="rounded-lg bg-[#003049] px-4 py-2.5 text-sm font-bold text-white transition hover:bg-[#669bbc]"
            >
              Registrar dispositivo
            </button>
          </>
        }
      />

      {message && (
        <div className="rounded-lg border border-[#669bbc]/20 bg-[#fdf0d5] px-4 py-3 text-sm font-medium text-[#003049]">
          {message}
        </div>
      )}

      {loading ? (
        <div className="rounded-xl border border-[#669bbc]/20 bg-white p-8 text-sm text-slate-500">
          Cargando infraestructura…
        </div>
      ) : devices.length === 0 ? (
        <div className="rounded-xl border border-dashed border-[#669bbc]/40 bg-[#fdf0d5] p-8 text-sm text-slate-600">
          No hay dispositivos registrados.
        </div>
      ) : (
        <DeviceObservatory devices={devices} syncing={syncing} onSync={handleSync} />
      )}

      {showForm && (
        <DeviceForm onClose={() => setShowForm(false)} onSubmit={handleCreate} />
      )}
    </div>
  );
}

function DeviceForm({ onClose, onSubmit }) {
  const [form, setForm] = useState({
    name: "",
    ip: "",
    port: 4370,
    interval_seconds: 300,
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      [name]: name === "port" || name === "interval_seconds" ? Number(value) : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    await onSubmit(form);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#003049]/60 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
        <div className="mb-5">
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#780000]">New endpoint</p>
          <h2 className="mt-1 text-xl font-bold text-[#003049]">Registrar dispositivo</h2>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            ["name", "Nombre operativo", "text"],
            ["ip", "IP o endpoint", "text"],
            ["port", "Puerto", "number"],
            ["interval_seconds", "Intervalo en segundos", "number"],
          ].map(([name, label, type]) => (
            <label key={name} className="block text-sm font-medium text-slate-600">
              {label}
              <input
                name={name}
                type={type}
                value={form[name]}
                onChange={handleChange}
                required
                className="mt-1 w-full rounded-lg border border-[#669bbc]/30 px-3 py-2.5 text-[#003049] outline-none focus:border-[#c1121f] focus:ring-2 focus:ring-[#c1121f]/10"
              />
            </label>
          ))}
          <div className="flex justify-end gap-3 pt-3">
            <button type="button" onClick={onClose} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600">
              Cancelar
            </button>
            <button type="submit" className="rounded-lg bg-[#c1121f] px-4 py-2 text-sm font-bold text-white hover:bg-[#780000]">
              Guardar dispositivo
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

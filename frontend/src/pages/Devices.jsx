import { useEffect, useState } from "react";
import {
  getDevices,
  createDevice,
  syncDevice,
  syncAllDevices,
} from "../api/devices.api";
import { useDeviceStatus } from "../hooks/useDeviceStatus";

/* =========================
   DeviceForm (LOCAL)
========================= */
function DeviceForm({ onClose, onSubmit }) {
  const [form, setForm] = useState({
    name: "",
    ip: "",
    port: 4370,
    interval_seconds: 300,
  });

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === "port" || name === "interval_seconds"
        ? Number(value)
        : value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    await onSubmit(form);
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 className="text-lg font-semibold mb-4">
          Registrar dispositivo
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="name"
            placeholder="Nombre del dispositivo"
            className="w-full border rounded px-3 py-2"
            onChange={handleChange}
            required
          />

          <input
            name="ip"
            placeholder="IP (ej: 192.168.1.100)"
            className="w-full border rounded px-3 py-2"
            onChange={handleChange}
            required
          />

          <input
            name="port"
            type="number"
            className="w-full border rounded px-3 py-2"
            onChange={handleChange}
          />

          <input
            name="interval_seconds"
            type="number"
            className="w-full border rounded px-3 py-2"
            onChange={handleChange}
          />

          <div className="flex justify-end gap-2 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded border"
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* =========================
   Devices Page
========================= */
export default function Devices() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [syncing, setSyncing] = useState(null);
  const [message, setMessage] = useState("");

  useDeviceStatus((event) => {
    if (event.type === "device_snapshot") {
      setDevices(event.devices);
      return;
    }
    if (event.type === "device_status_changed") {
      setDevices((current) =>
        current.map((device) =>
          device.id === event.device_id || device.device_id === event.device_id
            ? { ...device, status: event.status }
            : device,
        ),
      );
    }
  });

  useEffect(() => {
    loadDevices();
  }, []);

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
    } catch (e) {
      console.error(e);
      setDevices([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(device) {
    await createDevice(device);
    setShowForm(false);
    loadDevices();
  }

  async function handleSync(deviceId) {
    setSyncing(deviceId);
    setMessage("");
    try {
      const result = await syncDevice(deviceId);
      setMessage(
        result.status === "completed"
          ? "Sincronización completada"
          : "Sincronización enviada a la cola",
      );
      await loadDevices();
    } catch (error) {
      console.error(error);
      setMessage("No se pudo iniciar la sincronización");
    } finally {
      setSyncing(null);
    }
  }

  async function handleSyncAll() {
    setSyncing("all");
    setMessage("");
    try {
      const result = await syncAllDevices();
      setMessage(
        result.status === "completed"
          ? "Sincronización demo completada"
          : "Sincronizaciones enviadas a la cola",
      );
      await loadDevices();
    } catch (error) {
      console.error(error);
      setMessage("No se pudo iniciar la sincronización");
    } finally {
      setSyncing(null);
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Dispositivos</h1>

        <div className="flex gap-2">
          <button
            onClick={handleSyncAll}
            disabled={syncing !== null}
            className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition disabled:opacity-50"
          >
            {syncing === "all" ? "Sincronizando…" : "Sincronizar todo"}
          </button>
          <button
            onClick={() => setShowForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            + Registrar dispositivo
          </button>
        </div>
      </div>

      {message && (
        <div className="mb-4 rounded-lg bg-blue-50 px-4 py-3 text-blue-700">
          {message}
        </div>
      )}

      {loading ? (
        <div className="text-gray-500">Cargando dispositivos…</div>
      ) : devices.length === 0 ? (
        <div className="text-gray-500">No hay dispositivos registrados</div>
      ) : (
        <div className="overflow-x-auto border rounded-lg">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left">Nombre</th>
                <th className="px-4 py-3 text-left">IP</th>
                <th className="px-4 py-3 text-left">Estado</th>
                <th className="px-4 py-3 text-left">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((d) => (
                <tr key={d.id} className="border-t hover:bg-gray-50">
                  <td className="px-4 py-2">{d.name}</td>
                  <td className="px-4 py-2">{d.ip}</td>
                  <td className="px-4 py-2">
                    <span className={`inline-flex items-center gap-2 ${
                      d.status === "error"
                        ? "text-red-600"
                        : d.status === "connected" || d.status === "healthy"
                          ? "text-green-600"
                          : "text-slate-500"
                    }`}>
                      <span className={`w-2 h-2 rounded-full ${
                        d.status === "error"
                          ? "bg-red-500"
                          : d.status === "connected" || d.status === "healthy"
                            ? "bg-green-500"
                            : "bg-slate-400"
                      }`}></span>
                      {d.status === "healthy"
                        ? "Saludable"
                        : d.status === "connected"
                          ? "Conectado"
                          : d.status === "connecting"
                            ? "Conectando…"
                            : d.status === "error"
                              ? "Error"
                              : d.status === "disabled"
                                ? "Inactivo"
                                : "Sin estado"}
                    </span>
                  </td>
                  <td className="px-4 py-2">
                    <button
                      onClick={() => handleSync(d.device_id ?? d.id)}
                      disabled={syncing !== null}
                      className="text-blue-600 hover:underline disabled:opacity-50"
                    >
                      {syncing === (d.device_id ?? d.id)
                        ? "Procesando…"
                        : "Sincronizar"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showForm && (
        <DeviceForm
          onClose={() => setShowForm(false)}
          onSubmit={handleCreate}
        />
      )}
    </div>
  );
}

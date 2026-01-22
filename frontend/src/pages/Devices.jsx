import { useEffect, useState } from "react";
import { getDevices, createDevice } from "../api/devices.api";

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

  useEffect(() => {
    loadDevices();
  }, []);

  async function loadDevices() {
    try {
      const data = await getDevices();
      setDevices(Array.isArray(data) ? data : []);
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

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Dispositivos</h1>

        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          + Registrar dispositivo
        </button>
      </div>

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
              </tr>
            </thead>
            <tbody>
              {devices.map((d) => (
                <tr key={d.id} className="border-t hover:bg-gray-50">
                  <td className="px-4 py-2">{d.name}</td>
                  <td className="px-4 py-2">{d.ip}</td>
                  <td className="px-4 py-2">
                    <span className="inline-flex items-center gap-2 text-green-600">
                      <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                      Activo
                    </span>
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

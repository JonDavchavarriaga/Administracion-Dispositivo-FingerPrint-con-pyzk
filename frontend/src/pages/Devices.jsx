import { useEffect, useState } from "react";
import { getDevices, createDevice } from "../api/client";

export default function Devices() {
  const [devices, setDevices] = useState([]);
  const [form, setForm] = useState({
    name: "",
    ip: "",
    port: 4370,
    interval_seconds: 300,
  });

  async function loadDevices() {
    const data = await getDevices();
    setDevices(data);
  }

  useEffect(() => {
    loadDevices();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    await createDevice(form);
    setForm({ name: "", ip: "", port: 4370, interval_seconds: 300 });
    loadDevices();
  }

  return (
    <div>
      <h2>Dispositivos</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Nombre"
          value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })}
        />
        <input
          placeholder="IP"
          value={form.ip}
          onChange={e => setForm({ ...form, ip: e.target.value })}
        />
        <button>Registrar</button>
      </form>

      <ul>
        {devices.map(d => (
          <li key={d.device_id}>
            {d.name} – {d.ip} – {d.active ? "Activo" : "Inactivo"}
          </li>
        ))}
      </ul>
    </div>
  );
}

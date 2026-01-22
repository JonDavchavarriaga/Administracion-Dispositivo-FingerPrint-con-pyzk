import { useEffect, useState } from "react";
import { getAttendance } from "../api/client";

export default function Attendance() {
  const [records, setRecords] = useState([]);      // SIEMPRE array
  const [loading, setLoading] = useState(true);    // estado de carga
  const [error, setError] = useState(null);         // estado de error

  useEffect(() => {
    let mounted = true;

    async function loadAttendance() {
      try {
        const data = await getAttendance();

        if (!mounted) return;

        // Blindaje duro
        if (Array.isArray(data)) {
          setRecords(data);
        } else {
          console.warn("Attendance API did not return an array:", data);
          setRecords([]);
        }
      } catch (err) {
        console.error("Error loading attendance:", err);
        if (mounted) {
          setError("No se pudo cargar la asistencia");
          setRecords([]);
        }
      } finally {
        if (mounted) setLoading(false);
      }
    }

    loadAttendance();

    return () => {
      mounted = false;
    };
  }, []);

  // -------- RENDER STATES --------

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64 text-gray-500">
        Cargando asistencia…
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64 text-red-500">
        {error}
      </div>
    );
  }

  if (records.length === 0) {
    return (
      <div className="flex justify-center items-center h-64 text-gray-500">
        No hay registros de asistencia
      </div>
    );
  }

  // -------- TABLE --------

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Asistencia</h1>

      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-gray-100 text-gray-700">
            <tr>
              <th className="px-4 py-3">Usuario</th>
              <th className="px-4 py-3">Dispositivo</th>
              <th className="px-4 py-3">Fecha / Hora</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r, index) => (
              <tr
                key={index}
                className="border-t hover:bg-gray-50 transition"
              >
                <td className="px-4 py-2">{r.user_id}</td>
                <td className="px-4 py-2">{r.device_id}</td>
                <td className="px-4 py-2">
                  {new Date(r.timestamp).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

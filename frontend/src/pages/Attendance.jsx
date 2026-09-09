import { useEffect, useMemo, useState } from "react";
import { getAttendance } from "../api/attendance.api";
import { useDeviceStatus } from "../hooks/useDeviceStatus";
import ActivityStream from "../components/dashboard/ActivityStream";
import DashboardHeader from "../components/dashboard/DashboardHeader";
import MetricsOverview from "../components/dashboard/MetricsOverview";
import SystemNarrative from "../components/dashboard/SystemNarrative";

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [liveStatus, setLiveStatus] = useState("connected");
  const [lastUpdate, setLastUpdate] = useState(new Date());

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

  const metrics = [
    {
      label: "Marcaciones procesadas",
      value: records.length,
      badge: "5 min",
      caption: "Eventos recibidos por la plataforma",
      tone: "blue",
    },
    {
      label: "Personas identificadas",
      value: uniqueUsers,
      badge: "Únicas",
      caption: "Cédulas presentes en la operación",
      tone: "red",
    },
    {
      label: "Telemetría",
      value: liveStatus === "attention" ? "Atención" : "En línea",
      badge: lastUpdate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      caption: "Estado del canal de eventos",
      tone: "steel",
    },
  ];

  return (
    <div className="space-y-8">
      <DashboardHeader
        title="Centro operativo"
        description="Una vista ejecutiva de la asistencia, la actividad biométrica y la salud de la operación."
      />
      <MetricsOverview metrics={metrics} />
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ActivityStream records={[...records].reverse().slice(0, 30)} loading={loading} />
        </div>
        <SystemNarrative />
      </div>
    </div>
  );
}

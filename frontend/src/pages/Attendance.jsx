import { useEffect, useState } from "react";
import { getAttendance } from "../api/client";

export default function Attendance() {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    getAttendance().then(setRecords);
  }, []);

  return (
    <div>
      <h2>Marcaciones</h2>

      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Device ID</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {records.map((r, i) => (
            <tr key={i}>
              <td>{r.user_id}</td>
              <td>{r.device_id}</td>
              <td>{new Date(r.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

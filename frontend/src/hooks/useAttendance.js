import { useEffect, useState } from "react";
import { getAttendance } from "../api/attendance.api";

export function useAttendance() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAttendance()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading };
}

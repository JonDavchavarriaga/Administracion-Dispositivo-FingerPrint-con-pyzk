const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getDevices() {
  const res = await fetch(`${API_URL}/devices`);
  return res.json();
}

export async function createDevice(device) {
  const res = await fetch(`${API_URL}/devices`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(device),
  });
  return res.json();
}

export async function getAttendance() {
  const res = await fetch(`${API_URL}/attendance`);
  return res.json();
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function httpGet(path) {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) throw new Error("Error en petición");
  return res.json();
}

export async function httpPost(path, data) {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Error en petición");
  return res.json();
}

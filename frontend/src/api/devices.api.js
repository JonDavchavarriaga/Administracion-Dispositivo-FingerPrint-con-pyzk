import api from "./client";

export async function getDevices() {
  const { data } = await api.get("/devices");
  return data;
}

export async function createDevice(device) {
  const { data } = await api.post("/devices", device);
  return data;
}

export async function syncDevice(deviceId) {
  const { data } = await api.post(`/devices/${deviceId}/sync`);
  return data;
}

export async function syncAllDevices() {
  const { data } = await api.post("/devices/sync-all");
  return data;
}

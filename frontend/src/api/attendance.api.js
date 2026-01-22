import api from "./client";

export async function getAttendance() {
  const { data } = await api.get("/attendance");
  return data;
}

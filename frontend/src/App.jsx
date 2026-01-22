import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/layouts/Layouts";
import Attendance from "./pages/Attendance";
import Devices from "./pages/Devices";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/attendance" />} />
          <Route path="/attendance" element={<Attendance />} />
          <Route path="/devices" element={<Devices />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

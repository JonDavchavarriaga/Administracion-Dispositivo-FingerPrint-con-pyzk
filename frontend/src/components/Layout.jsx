import { Link } from "react-router-dom";

export default function Layout({ children }) {
  return (
    <div>
      <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
        <Link to="/devices">Dispositivos</Link>{" | "}
        <Link to="/attendance">Marcaciones</Link>
      </nav>

      <main style={{ padding: "1rem" }}>
        {children}
      </main>
    </div>
  );
}

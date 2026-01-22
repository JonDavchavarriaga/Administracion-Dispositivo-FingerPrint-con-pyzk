import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-slate-100 min-h-screen flex flex-col">

      {/* Branding */}
      <div className="px-6 py-8 border-b border-slate-700">
        <h2 className="text-lg font-semibold tracking-wide">
          Panel
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Control de Asistencia
        </p>
      </div>

      {/* Navegación */}
      <nav className="flex-1 px-4 py-6 space-y-3">
        <Link
          to="/attendance"
          className="block px-4 py-3 rounded-lg hover:bg-slate-800 transition"
        >
          📋 Asistencia
        </Link>

        <Link
          to="/devices"
          className="block px-4 py-3 rounded-lg hover:bg-slate-800 transition"
        >
          🔌 Dispositivos
        </Link>
      </nav>

      {/* Footer sidebar */}
      <div className="px-6 py-4 text-xs text-slate-500 border-t border-slate-700">
        v0.1.0
      </div>
    </aside>
  );
}


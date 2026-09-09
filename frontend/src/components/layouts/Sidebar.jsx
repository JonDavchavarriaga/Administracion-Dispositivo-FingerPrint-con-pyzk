import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-72 bg-[#003049] text-slate-100 min-h-screen flex flex-col">

      {/* Branding */}
      <div className="px-7 py-8 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-2xl bg-[#c1121f] flex items-center justify-center shadow-lg shadow-black/20">
            <span className="text-xl">⌁</span>
          </div>
          <div>
            <h2 className="text-lg font-bold tracking-tight">NEXUS</h2>
            <p className="text-[11px] uppercase tracking-[0.2em] text-[#669bbc]">
              Workforce intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Navegación */}
      <nav className="flex-1 px-4 py-7 space-y-2">
        <p className="px-4 mb-3 text-[10px] uppercase tracking-[0.22em] text-[#669bbc]">
          Operación
        </p>
        <Link
          to="/attendance"
          className="block px-4 py-3 rounded-xl hover:bg-white/10 transition font-medium"
        >
          <span className="mr-3 text-[#fdf0d5]">◈</span> Centro operativo
        </Link>

        <Link
          to="/devices"
          className="block px-4 py-3 rounded-xl hover:bg-white/10 transition font-medium"
        >
          <span className="mr-3 text-[#fdf0d5]">◉</span> Red biométrica
        </Link>
      </nav>

      {/* Footer sidebar */}
      <div className="px-6 py-5 text-xs text-[#669bbc] border-t border-white/10">
        <p className="text-white/80">Demo environment</p>
        <p className="mt-1">v1.0 · Live telemetry</p>
      </div>
    </aside>
  );
}

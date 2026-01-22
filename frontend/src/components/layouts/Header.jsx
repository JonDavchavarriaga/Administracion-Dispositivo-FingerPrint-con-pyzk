export default function Header() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-center px-6">
      <div className="flex items-center gap-3">
        {/* Logo (puede ser img más adelante) */}
        <div className="w-9 h-9 rounded bg-slate-900 text-white flex items-center justify-center font-bold">
          H
        </div>

        <span className="text-xl font-semibold text-slate-800">
          Nombre de la Empresa
        </span>
      </div>
    </header>
  );
}

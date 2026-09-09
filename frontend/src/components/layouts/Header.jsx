export default function Header() {
  return (
    <header className="h-20 bg-[#fdf0d5] border-b border-[#003049]/10 flex items-center justify-between px-8">
      <div>
        <p className="text-[10px] uppercase tracking-[0.22em] text-[#780000] font-bold">
          Biometric operations center
        </p>
        <h1 className="text-xl font-bold text-[#003049] mt-1">
          NEXUS Workforce Intelligence
        </h1>
      </div>
      <div className="flex items-center gap-3">
        <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
        <span className="text-sm font-medium text-[#003049]">Demo en vivo</span>
        <div className="w-9 h-9 rounded-full bg-[#003049] text-[#fdf0d5] flex items-center justify-center font-bold">
          AD
        </div>
      </div>
    </header>
  );
}

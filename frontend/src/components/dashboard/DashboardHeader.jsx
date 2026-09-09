export default function DashboardHeader({
  eyebrow = "Biometric operations center",
  title,
  description,
  action,
}) {
  return (
    <section className="flex flex-col gap-5 border-b border-[#669bbc]/20 pb-6 lg:flex-row lg:items-end lg:justify-between">
      <div className="min-w-0">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#780000]">
          {eyebrow}
        </p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-[#003049]">
          {title}
        </h1>
        {description && (
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
            {description}
          </p>
        )}
      </div>
      {action && <div className="flex shrink-0 flex-wrap gap-3">{action}</div>}
    </section>
  );
}

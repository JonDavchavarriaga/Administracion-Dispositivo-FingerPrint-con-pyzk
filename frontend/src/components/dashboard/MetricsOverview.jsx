const tones = {
  blue: "bg-[#fdf0d5] text-[#003049]",
  red: "bg-[#fff0f0] text-[#780000]",
  steel: "bg-[#edf5f7] text-[#003049]",
};

export default function MetricsOverview({ metrics }) {
  return (
    <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
      {metrics.map((metric) => (
        <article
          key={metric.label}
          className="rounded-xl border border-[#669bbc]/20 bg-[#fdf0d5] p-5 shadow-sm"
        >
          <div className="flex items-start justify-between gap-4">
            <p className="text-sm font-medium text-slate-600">{metric.label}</p>
            <span
              className={`rounded-lg px-2.5 py-1 text-xs font-bold ${tones[metric.tone] || tones.blue}`}
            >
              {metric.badge}
            </span>
          </div>
          <p className="mt-4 text-3xl font-bold tracking-tight text-[#003049]">
            {metric.value}
          </p>
          <p className="mt-1 text-xs text-slate-500">{metric.caption}</p>
        </article>
      ))}
    </section>
  );
}

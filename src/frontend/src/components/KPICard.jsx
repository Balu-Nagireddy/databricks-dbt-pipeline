/** Reusable KPI card with icon, value, label, and glow color. */
export function KPICard({ icon, value, label, color = '#6366f1', loading }) {
  return (
    <div className="card kpi-card">
      <div className="kpi-card__glow" style={{ background: color }} />
      <div className="kpi-card__icon" style={{ background: `${color}22` }}>
        {icon}
      </div>
      {loading
        ? <div className="skeleton skeleton-kpi" style={{ marginBottom: 8 }} />
        : <div className="kpi-card__value">{value}</div>
      }
      <div className="kpi-card__label">{label}</div>
    </div>
  )
}

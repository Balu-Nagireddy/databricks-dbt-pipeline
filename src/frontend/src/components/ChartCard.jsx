/** Generic chart wrapper card — title + children (any Recharts chart). */
export function ChartCard({ title, children, className = '' }) {
  return (
    <div className={`card ${className}`}>
      <div className="card__title">{title}</div>
      {children}
    </div>
  )
}

/** Skeleton row grid for loading chart placeholders. */
export function ChartSkeleton({ height = 200 }) {
  return (
    <div className="skeleton" style={{ height, borderRadius: 8 }} />
  )
}

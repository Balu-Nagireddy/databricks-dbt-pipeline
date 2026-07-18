/** Shared utility functions — no business logic, presentation only. */

export function fmt(n, decimals = 1) {
  if (n == null) return '—'
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(decimals)}M`
  if (n >= 1_000)     return `${(n / 1_000).toFixed(decimals)}K`
  return n.toLocaleString()
}

export function fmtCurrency(n, decimals = 1) {
  if (n == null) return '—'
  if (n >= 1_000_000) return `R$ ${(n / 1_000_000).toFixed(decimals)}M`
  if (n >= 1_000)     return `R$ ${(n / 1_000).toFixed(decimals)}K`
  return `R$ ${Number(n).toFixed(2)}`
}

export function fmtPct(n, decimals = 1) {
  if (n == null) return '—'
  return `${Number(n).toFixed(decimals)}%`
}

export function fmtDays(n, decimals = 1) {
  if (n == null) return '—'
  return `${Number(n).toFixed(decimals)}d`
}

export function segmentBadge(seg) {
  const map = { VIP: 'badge-indigo', 'High Value': 'badge-teal', Standard: 'badge-amber' }
  return map[seg] || 'badge-amber'
}

export const CHART_COLORS = ['#6366f1','#14b8a6','#f59e0b','#f43f5e','#10b981','#8b5cf6','#38bdf8']

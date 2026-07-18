/**
 * Centralized API client.
 * All calls route through Vite dev proxy or deployed Vercel domain → FastAPI backend.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const BASE = `${BASE_URL}/api/v1`

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

// ── Health ──────────────────────────────────────────────────
export const api = {
  health:       () => request('/health'),
  version:      () => request('/health/version'),

  // Executive
  kpis:         () => request('/executive/kpis'),

  // Sales
  salesDaily:   (params = {}) => request('/sales/daily?'   + new URLSearchParams(params)),
  salesMonthly: (params = {}) => request('/sales/monthly?' + new URLSearchParams(params)),
  salesByState: (params = {}) => request('/sales/by-state?'+ new URLSearchParams(params)),

  // Customers
  customerSegments: (params = {}) => request('/customers/segments?'   + new URLSearchParams(params)),
  topCities:        (params = {}) => request('/customers/top-cities?' + new URLSearchParams(params)),
  repeatStats:      ()            => request('/customers/repeat-stats'),

  // Products
  topProducts:   (params = {}) => request('/products/top?'        + new URLSearchParams(params)),
  categories:    (params = {}) => request('/products/categories?' + new URLSearchParams(params)),

  // Finance
  payments:      () => request('/finance/payments'),
  installments:  () => request('/finance/installments'),

  // Logistics
  logisticsPerf: (params = {}) => request('/logistics/performance?'     + new URLSearchParams(params)),
  successRates:  ()             => request('/logistics/success-rates'),
  sellerShipping:(params = {}) => request('/logistics/seller-shipping?' + new URLSearchParams(params)),
}

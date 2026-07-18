import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useLogisticsPerf, useSuccessRates, useSellerShipping } from '../../hooks/useData'
import { ChartCard, ChartSkeleton } from '../../components/ChartCard'
import { KPICard } from '../../components/KPICard'
import { ErrorState, EmptyState } from '../../components/States'
import { fmt, fmtDays, fmtPct, CHART_COLORS } from '../../utils/format'
import { CheckCircle, Clock, AlertCircle, Package } from 'lucide-react'

export default function LogisticsPage() {
  const perf     = useLogisticsPerf({ limit: 27 })
  const success  = useSuccessRates()
  const shipping = useSellerShipping({ limit: 50 })

  const d = success.data

  const kpis = [
    { icon: <Package size={18} />,      value: fmt(d?.total_orders),      label: 'Total Orders',     color: '#6366f1' },
    { icon: <CheckCircle size={18} />,  value: fmt(d?.total_delivered),   label: 'On-Time Delivered',color: '#10b981' },
    { icon: <AlertCircle size={18} />,  value: fmt(d?.total_late_orders), label: 'Late Orders',      color: '#f43f5e' },
    { icon: <Clock size={18} />,        value: fmtPct(d?.success_rate_percent), label: 'On-Time Rate', color: '#14b8a6' },
  ]

  const perfData = (perf.data ?? []).slice(0, 15).map(r => ({
    state: r.customer_state,
    days: r.avg_delivery_duration_days,
    orders: r.total_orders,
  }))

  const shipData = (shipping.data ?? []).slice(0, 20).map(r => ({
    id: r.seller_id?.slice(0, 8),
    days: r.avg_shipping_duration_days,
    items: r.items_shipped,
  }))

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-header__title">Logistics Analytics</h1>
          <p className="page-header__sub">Delivery performance, state analysis &amp; seller shipping</p>
        </div>
      </div>

      <div className="page-body">
        {/* KPI row */}
        <div className="grid grid-4">
          {kpis.map((k, i) => <KPICard key={i} {...k} loading={success.isLoading} />)}
        </div>

        <div className="grid grid-2">
          {/* Avg delivery days by state */}
          <ChartCard title="Avg Delivery Days by State">
            {perf.isLoading ? <ChartSkeleton height={260} /> :
             perf.isError   ? <ErrorState /> :
             perfData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={perfData} layout="vertical" margin={{ left: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" tickFormatter={v => `${v.toFixed(1)}d`} />
                  <YAxis type="category" dataKey="state" width={28} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={v => `${Number(v).toFixed(1)} days`} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                  <Bar dataKey="days" fill={CHART_COLORS[2]} name="Avg Delivery Days" radius={[0,4,4,0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>

          {/* Seller shipping duration */}
          <ChartCard title="Top 20 Sellers — Avg Shipping Duration">
            {shipping.isLoading ? <ChartSkeleton height={260} /> :
             shipping.isError   ? <ErrorState /> :
             shipData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={shipData} layout="vertical" margin={{ left: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" tickFormatter={v => `${v?.toFixed(1)}d`} />
                  <YAxis type="category" dataKey="id" width={60} tick={{ fontSize: 10 }} />
                  <Tooltip formatter={v => v != null ? `${Number(v).toFixed(1)} days` : 'N/A'} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                  <Bar dataKey="days" fill={CHART_COLORS[4]} name="Avg Shipping Days" radius={[0,4,4,0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
        </div>

        {/* Full state table */}
        <div className="card">
          <div className="card__title">Delivery Performance by State</div>
          {perf.isLoading ? (
            <div>{[...Array(6)].map((_,i) => <div key={i} className="skeleton skeleton-text" />)}</div>
          ) : perf.isError ? <ErrorState /> : (
            <div className="table-wrapper">
              <table className="data-table">
                <thead><tr><th>State</th><th>Total Orders</th><th>Avg Delivery Days</th></tr></thead>
                <tbody>
                  {(perf.data ?? []).map(r => (
                    <tr key={r.customer_state}>
                      <td><strong>{r.customer_state}</strong></td>
                      <td>{fmt(r.total_orders)}</td>
                      <td>{fmtDays(r.avg_delivery_duration_days)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

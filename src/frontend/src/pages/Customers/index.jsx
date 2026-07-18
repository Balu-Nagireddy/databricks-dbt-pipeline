import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { useCustomerSegments, useTopCities, useRepeatStats } from '../../hooks/useData'
import { ChartCard, ChartSkeleton } from '../../components/ChartCard'
import { ErrorState, EmptyState } from '../../components/States'
import { fmtCurrency, fmt, segmentBadge, CHART_COLORS } from '../../utils/format'

export default function CustomersPage() {
  const segments   = useCustomerSegments({ limit: 50 })
  const cities     = useTopCities({ limit: 15 })
  const repeatData = useRepeatStats()

  // Segment summary for pie chart
  const segSummary = Object.entries(
    (segments.data ?? []).reduce((acc, r) => {
      acc[r.customer_segment] = (acc[r.customer_segment] || 0) + 1
      return acc
    }, {})
  ).map(([name, value]) => ({ name, value }))

  const cityData = (cities.data ?? []).slice(0, 10).map(r => ({
    city: r.customer_city,
    customers: r.customer_count,
  }))

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-header__title">Customer Analytics</h1>
          <p className="page-header__sub">CLV segmentation, top cities & repeat behaviour</p>
        </div>
      </div>

      <div className="page-body">
        <div className="grid grid-2" style={{ marginBottom: 20 }}>
          {/* Segment Pie */}
          <ChartCard title="Customer Segment Distribution">
            {segments.isLoading ? <ChartSkeleton height={220} /> :
             segments.isError   ? <ErrorState /> : (
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie data={segSummary} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, percent }) => `${name} (${(percent*100).toFixed(0)}%)`} labelLine={false}>
                    {segSummary.map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </ChartCard>

          {/* Repeat customers */}
          <ChartCard title="Repeat vs One-Time Customers">
            {repeatData.isLoading ? <ChartSkeleton height={220} /> :
             repeatData.isError   ? <ErrorState /> :
             (repeatData.data ?? []).length === 0 ? <EmptyState /> : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 16, paddingTop: 16 }}>
                {(repeatData.data ?? []).map(r => (
                  <div key={String(r.is_repeat_customer)}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                      <span>{r.is_repeat_customer ? 'Repeat Customers' : 'One-Time Customers'}</span>
                      <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{fmt(r.customer_count)}</span>
                    </div>
                    <div className="progress-bar">
                      <div className="progress-bar__fill" style={{ width: `${Math.min((r.customer_count / (repeatData.data.reduce((a,b) => a + b.customer_count, 0))) * 100, 100)}%`, background: r.is_repeat_customer ? '#6366f1' : '#14b8a6' }} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </ChartCard>
        </div>

        {/* Top cities */}
        <ChartCard title="Top 10 Cities by Customer Count" className="col-span-2">
          {cities.isLoading ? <ChartSkeleton height={240} /> :
           cities.isError   ? <ErrorState /> :
           cityData.length === 0 ? <EmptyState /> : (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={cityData} layout="vertical" margin={{ left: 10 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" tickFormatter={fmt} />
                <YAxis type="category" dataKey="city" width={90} tick={{ fontSize: 10 }} />
                <Tooltip formatter={fmt} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                <Bar dataKey="customers" fill={CHART_COLORS[2]} name="Customers" radius={[0,4,4,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </ChartCard>

        {/* CLV Table */}
        <div className="card" style={{ marginTop: 20 }}>
          <div className="card__title">Top Customers by Lifetime Value</div>
          {segments.isLoading ? (
            <div>{[...Array(6)].map((_, i) => <div key={i} className="skeleton skeleton-text" style={{ marginBottom: 10 }} />)}</div>
          ) : segments.isError ? <ErrorState /> : (
            <div style={{ overflowX: 'auto' }}>
              <table className="data-table">
                <thead><tr><th>Customer ID</th><th>Orders</th><th>Lifetime Value</th><th>Avg Spend</th><th>Segment</th></tr></thead>
                <tbody>
                  {(segments.data ?? []).slice(0, 20).map(r => (
                    <tr key={r.customer_unique_id}>
                      <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{r.customer_unique_id?.slice(0, 8)}…</td>
                      <td>{r.total_orders}</td>
                      <td>{fmtCurrency(r.lifetime_value)}</td>
                      <td>{fmtCurrency(r.avg_order_spend)}</td>
                      <td><span className={`badge ${segmentBadge(r.customer_segment)}`}>{r.customer_segment}</span></td>
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

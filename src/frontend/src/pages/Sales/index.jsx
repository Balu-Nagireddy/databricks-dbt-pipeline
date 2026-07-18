import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { useSalesDaily, useSalesMonthly, useSalesByState } from '../../hooks/useData'
import { ChartCard, ChartSkeleton } from '../../components/ChartCard'
import { ErrorState, EmptyState } from '../../components/States'
import { fmtCurrency, fmt, CHART_COLORS } from '../../utils/format'

export default function SalesPage() {
  const daily   = useSalesDaily({ limit: 60 })
  const monthly = useSalesMonthly({ limit: 24 })
  const byState = useSalesByState({ limit: 27 })

  const dailyData = [...(daily.data ?? [])].reverse().map(r => ({
    date: r.sale_date?.slice(5) ?? r.sale_date,
    revenue: r.total_revenue,
    orders: r.total_orders,
  }))

  const monthlyData = [...(monthly.data ?? [])].reverse().map(r => ({
    month: String(r.sale_month).slice(0, 7),
    revenue: r.total_revenue,
    orders: r.total_orders,
  }))

  const stateData = (byState.data ?? []).slice(0, 10).map(r => ({
    state: r.customer_state,
    revenue: r.total_revenue,
    orders: r.total_orders,
  }))

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-header__title">Sales Analytics</h1>
          <p className="page-header__sub">Revenue trends, daily &amp; monthly time-series</p>
        </div>
      </div>

      <div className="page-body">
        <div className="grid grid-1">

          {/* Daily Revenue */}
          <ChartCard title="Daily Revenue Trend (last 60 days)">
            {daily.isLoading ? <ChartSkeleton height={240} /> :
             daily.isError   ? <ErrorState /> :
             dailyData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={dailyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} interval={9} />
                  <YAxis tickFormatter={v => fmtCurrency(v)} width={72} />
                  <Tooltip formatter={v => fmtCurrency(v)} labelStyle={{ color: '#f1f5f9' }} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                  <Line type="monotone" dataKey="revenue" stroke={CHART_COLORS[0]} strokeWidth={2} dot={false} name="Revenue" />
                </LineChart>
              </ResponsiveContainer>
            )}
          </ChartCard>

          {/* Monthly Revenue */}
          <ChartCard title="Monthly Revenue &amp; Orders">
            {monthly.isLoading ? <ChartSkeleton height={240} /> :
             monthly.isError   ? <ErrorState /> :
             monthlyData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                  <YAxis tickFormatter={v => fmtCurrency(v)} width={72} />
                  <Tooltip formatter={v => fmtCurrency(v)} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                  <Legend />
                  <Bar dataKey="revenue" fill={CHART_COLORS[0]} name="Revenue" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>

          {/* Revenue by State */}
          <ChartCard title="Top 10 States by Revenue">
            {byState.isLoading ? <ChartSkeleton height={260} /> :
             byState.isError   ? <ErrorState /> :
             stateData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={stateData} layout="vertical" margin={{ left: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" tickFormatter={v => fmtCurrency(v)} />
                  <YAxis type="category" dataKey="state" width={30} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={v => fmtCurrency(v)} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                  <Bar dataKey="revenue" fill={CHART_COLORS[1]} name="Revenue" radius={[0,4,4,0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>

          {/* State table */}
          <div className="card">
            <div className="card__title">Revenue by State — Full Table</div>
            {byState.isLoading ? (
              <div>{[...Array(5)].map((_, i) => <div key={i} className="skeleton skeleton-text" />)}</div>
            ) : byState.isError ? <ErrorState /> : (
              <div className="table-wrapper">
                <table className="data-table">
                  <thead><tr><th>State</th><th>Total Revenue</th><th>Total Orders</th></tr></thead>
                  <tbody>
                    {(byState.data ?? []).map(r => (
                      <tr key={r.customer_state}>
                        <td><strong>{r.customer_state}</strong></td>
                        <td>{fmtCurrency(r.total_revenue)}</td>
                        <td>{fmt(r.total_orders)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

        </div>
      </div>
    </>
  )
}

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useTopProducts, useCategories } from '../../hooks/useData'
import { ChartCard, ChartSkeleton } from '../../components/ChartCard'
import { ErrorState, EmptyState } from '../../components/States'
import { fmtCurrency, fmt, CHART_COLORS } from '../../utils/format'

export default function ProductsPage() {
  const products   = useTopProducts({ limit: 50 })
  const categories = useCategories({ limit: 74 })

  const catData = (categories.data ?? []).slice(0, 12).map(r => ({
    cat: r.product_category_name_english?.replace(/_/g, ' '),
    revenue: r.total_revenue,
    units: r.units_sold,
  }))

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-header__title">Product Analytics</h1>
          <p className="page-header__sub">Top products by revenue and category performance</p>
        </div>
      </div>

      <div className="page-body">
        {/* Category revenue chart */}
        <ChartCard title="Top 12 Categories by Revenue">
          {categories.isLoading ? <ChartSkeleton height={280} /> :
           categories.isError   ? <ErrorState /> :
           catData.length === 0 ? <EmptyState /> : (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={catData} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" tickFormatter={v => fmtCurrency(v)} />
                <YAxis type="category" dataKey="cat" width={150} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(v, name) => name === 'revenue' ? fmtCurrency(v) : fmt(v)} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                <Bar dataKey="revenue" fill={CHART_COLORS[0]} name="Revenue" radius={[0,4,4,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </ChartCard>

        {/* Top products table */}
        <div className="card" style={{ marginTop: 20 }}>
          <div className="card__title">Top 50 Products by Revenue</div>
          {products.isLoading ? (
            <div>{[...Array(8)].map((_, i) => <div key={i} className="skeleton skeleton-text" style={{ marginBottom: 10 }} />)}</div>
          ) : products.isError ? <ErrorState /> : (products.data ?? []).length === 0 ? <EmptyState /> : (
            <div style={{ overflowX: 'auto' }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Product ID</th>
                    <th>Category</th>
                    <th>Units Sold</th>
                    <th>Revenue</th>
                    <th>Avg Price</th>
                  </tr>
                </thead>
                <tbody>
                  {(products.data ?? []).map((r, i) => (
                    <tr key={r.product_id}>
                      <td style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{i + 1}</td>
                      <td style={{ fontFamily: 'monospace', fontSize: '0.78rem' }}>{r.product_id?.slice(0, 10)}…</td>
                      <td>{r.product_category_name_english?.replace(/_/g, ' ')}</td>
                      <td>{fmt(r.units_sold)}</td>
                      <td style={{ color: 'var(--indigo-l)', fontWeight: 600 }}>{fmtCurrency(r.total_revenue)}</td>
                      <td>{fmtCurrency(r.avg_unit_price)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Category table */}
        <div className="card" style={{ marginTop: 20 }}>
          <div className="card__title">All Categories Performance</div>
          {categories.isLoading ? (
            <div>{[...Array(6)].map((_, i) => <div key={i} className="skeleton skeleton-text" style={{ marginBottom: 10 }} />)}</div>
          ) : categories.isError ? <ErrorState /> : (
            <div style={{ overflowX: 'auto' }}>
              <table className="data-table">
                <thead><tr><th>Category</th><th>Units Sold</th><th>Revenue</th><th>Avg Price</th></tr></thead>
                <tbody>
                  {(categories.data ?? []).map(r => (
                    <tr key={r.product_category_name_english}>
                      <td>{r.product_category_name_english?.replace(/_/g, ' ')}</td>
                      <td>{fmt(r.units_sold)}</td>
                      <td>{fmtCurrency(r.total_revenue)}</td>
                      <td>{fmtCurrency(r.avg_unit_price)}</td>
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

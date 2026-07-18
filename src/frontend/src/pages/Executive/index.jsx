import { DollarSign, ShoppingCart, Users, Package, Store, Star, Clock } from 'lucide-react'
import { useKPIs } from '../../hooks/useData'
import { KPICard } from '../../components/KPICard'
import { ErrorState } from '../../components/States'
import { fmtCurrency, fmt, fmtDays } from '../../utils/format'

const kpiConfig = (d) => [
  { icon: <DollarSign size={18} />, value: fmtCurrency(d?.total_revenue), label: 'Total Revenue',        color: '#6366f1' },
  { icon: <ShoppingCart size={18}/>, value: fmt(d?.total_orders),          label: 'Total Orders',         color: '#14b8a6' },
  { icon: <Users size={18} />,       value: fmt(d?.total_customers),       label: 'Total Customers',      color: '#8b5cf6' },
  { icon: <Store size={18} />,       value: fmt(d?.total_sellers),         label: 'Active Sellers',       color: '#f59e0b' },
  { icon: <Package size={18} />,     value: fmt(d?.total_products),        label: 'Products Listed',      color: '#f43f5e' },
  { icon: <Clock size={18} />,       value: fmtDays(d?.average_delivery_time_days), label: 'Avg Delivery Time', color: '#10b981' },
  { icon: <Star size={18} />,        value: d?.average_review_score?.toFixed(2) ?? '—', label: 'Avg Review Score', color: '#38bdf8' },
]

export default function ExecutivePage() {
  const { data, isLoading, isError } = useKPIs()

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-header__title">Executive Dashboard</h1>
          <p className="page-header__sub">Platform-wide KPIs at a glance</p>
        </div>
      </div>

      <div className="page-body">
        {isError ? (
          <ErrorState message="Unable to load KPI data from the API." />
        ) : (
          <>
            <div className="grid grid-4">
              {kpiConfig(data).slice(0, 4).map((k, i) => (
                <KPICard key={i} {...k} loading={isLoading} />
              ))}
            </div>
            <div className="grid grid-3">
              {kpiConfig(data).slice(4).map((k, i) => (
                <KPICard key={i} {...k} loading={isLoading} />
              ))}
            </div>

            {data && (
              <div className="card">
                <div className="card__title">Platform Summary</div>
                <div className="table-wrapper">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Metric</th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr><td>Total Revenue</td><td>{fmtCurrency(data.total_revenue, 2)}</td></tr>
                      <tr><td>Total Orders</td><td>{fmt(data.total_orders)}</td></tr>
                      <tr><td>Total Customers</td><td>{fmt(data.total_customers)}</td></tr>
                      <tr><td>Total Sellers</td><td>{fmt(data.total_sellers)}</td></tr>
                      <tr><td>Total Products</td><td>{fmt(data.total_products)}</td></tr>
                      <tr><td>Avg Delivery Time</td><td>{fmtDays(data.average_delivery_time_days)}</td></tr>
                      <tr><td>Avg Review Score</td><td>{data.average_review_score?.toFixed(2) ?? '—'} / 5.0</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </>
  )
}

import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { usePayments, useInstallments } from '../../hooks/useData'
import { ChartCard, ChartSkeleton } from '../../components/ChartCard'
import { ErrorState, EmptyState } from '../../components/States'
import { fmtCurrency, fmt, CHART_COLORS } from '../../utils/format'

export default function FinancePage() {
  const payments     = usePayments()
  const installments = useInstallments()

  const paymentData = (payments.data ?? []).map(r => ({
    name: r.payment_type?.charAt(0).toUpperCase() + r.payment_type?.slice(1),
    value: r.transaction_count,
    revenue: r.total_payment_value,
  }))

  const installData = (installments.data ?? []).map(r => ({
    inst: `${r.payment_installments}x`,
    transactions: r.transaction_count,
    value: r.total_payment_value,
  }))

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-header__title">Finance Analytics</h1>
          <p className="page-header__sub">Payment methods, installments &amp; transaction analysis</p>
        </div>
      </div>

      <div className="page-body">
        <div className="grid grid-2">
          {/* Payment method pie */}
          <ChartCard title="Payment Method Distribution (by transactions)">
            {payments.isLoading ? <ChartSkeleton height={240} /> :
             payments.isError   ? <ErrorState /> :
             paymentData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie data={paymentData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90}
                    label={({ name, percent }) => `${name} ${(percent*100).toFixed(0)}%`} labelLine={false}>
                    {paymentData.map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                  </Pie>
                  <Tooltip formatter={fmt} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </ChartCard>

          {/* Payment method revenue bar */}
          <ChartCard title="Payment Method — Revenue Breakdown">
            {payments.isLoading ? <ChartSkeleton height={240} /> :
             payments.isError   ? <ErrorState /> :
             paymentData.length === 0 ? <EmptyState /> : (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={paymentData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis tickFormatter={v => fmtCurrency(v)} width={72} />
                  <Tooltip formatter={v => fmtCurrency(v)} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                  <Bar dataKey="revenue" fill={CHART_COLORS[0]} name="Revenue" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
        </div>

        {/* Installments chart */}
        <ChartCard title="Transactions by Installment Count">
          {installments.isLoading ? <ChartSkeleton height={220} /> :
           installments.isError   ? <ErrorState /> :
           installData.length === 0 ? <EmptyState /> : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={installData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="inst" tick={{ fontSize: 11 }} />
                <YAxis tickFormatter={fmt} />
                <Tooltip formatter={(v, name) => name === 'value' ? fmtCurrency(v) : fmt(v)} contentStyle={{ background: '#1e2537', border: '1px solid #6366f133', borderRadius: 8 }} />
                <Legend />
                <Bar dataKey="transactions" fill={CHART_COLORS[1]} name="Transactions" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </ChartCard>

        {/* Payments summary table */}
        <div className="card">
          <div className="card__title">Payment Methods Summary</div>
          {payments.isLoading ? (
            <div>{[...Array(4)].map((_,i) => <div key={i} className="skeleton skeleton-text" />)}</div>
          ) : payments.isError ? <ErrorState /> : (
            <div className="table-wrapper">
              <table className="data-table">
                <thead><tr><th>Payment Type</th><th>Transactions</th><th>Total Value</th><th>Avg Transaction</th></tr></thead>
                <tbody>
                  {(payments.data ?? []).map(r => (
                    <tr key={r.payment_type}>
                      <td style={{ textTransform: 'capitalize', fontWeight: 500 }}>{r.payment_type}</td>
                      <td>{fmt(r.transaction_count)}</td>
                      <td style={{ color: 'var(--indigo-l)', fontWeight: 600 }}>{fmtCurrency(r.total_payment_value)}</td>
                      <td>{fmtCurrency(r.avg_transaction_value)}</td>
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

import { useLocation } from 'react-router-dom'

const titles = {
  '/':          { label: 'Executive',  sub: 'Platform-wide KPIs & business overview' },
  '/sales':     { label: 'Sales',      sub: 'Revenue trends, daily & monthly analytics' },
  '/customers': { label: 'Customers',  sub: 'Lifetime value, segmentation & city distribution' },
  '/products':  { label: 'Products',   sub: 'Top performers & category analysis' },
  '/finance':   { label: 'Finance',    sub: 'Payment methods & installment breakdown' },
  '/logistics': { label: 'Logistics',  sub: 'Delivery performance & shipping metrics' },
}

export function Topbar() {
  const { pathname } = useLocation()
  const meta = titles[pathname] || { label: pathname.slice(1), sub: '' }
  return (
    <header className="topbar">
      <div>
        <div className="topbar__breadcrumb">
          Prism Analytics Analytics / <span>{meta.label}</span>
        </div>
        {meta.sub && (
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 2 }}>
            {meta.sub}
          </div>
        )}
      </div>
      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        v1.0.0
      </div>
    </header>
  )
}

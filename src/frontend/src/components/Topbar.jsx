import { useLocation } from 'react-router-dom'
import { Menu } from 'lucide-react'

const titles = {
  '/':          { label: 'Executive',  sub: 'Platform-wide KPIs & business overview' },
  '/sales':     { label: 'Sales',      sub: 'Revenue trends, daily & monthly analytics' },
  '/customers': { label: 'Customers',  sub: 'Lifetime value, segmentation & city distribution' },
  '/products':  { label: 'Products',   sub: 'Top performers & category analysis' },
  '/finance':   { label: 'Finance',    sub: 'Payment methods & installment breakdown' },
  '/logistics': { label: 'Logistics',  sub: 'Delivery performance & shipping metrics' },
}

/**
 * Adaptive Topbar — shows hamburger button in overlay mode.
 * Props:
 *   navMode     — 'expanded' | 'compact' | 'overlay'
 *   onToggleNav — callback to toggle overlay sidebar
 */
export function Topbar({ navMode, onToggleNav }) {
  const { pathname } = useLocation()
  const meta = titles[pathname] || { label: pathname.slice(1), sub: '' }

  return (
    <header className="topbar" role="banner">
      <div className="topbar__left">
        {navMode === 'overlay' && (
          <button
            className="hamburger-btn"
            onClick={onToggleNav}
            aria-label="Toggle navigation menu"
            aria-expanded={false}
            type="button"
          >
            <Menu size={20} />
          </button>
        )}
        <div>
          <div className="topbar__breadcrumb">
            Prism Analytics / <span>{meta.label}</span>
          </div>
          {meta.sub && (
            <div className="topbar__sub">
              {meta.sub}
            </div>
          )}
        </div>
      </div>
      <div className="topbar__version">
        v1.0.0
      </div>
    </header>
  )
}

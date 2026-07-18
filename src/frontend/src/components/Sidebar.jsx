import { NavLink, useLocation } from 'react-router-dom'
import { useEffect, useRef } from 'react'
import {
  LayoutDashboard, TrendingUp, Users, Package,
  CreditCard, Truck
} from 'lucide-react'

const links = [
  { to: '/',          label: 'Executive',  icon: <LayoutDashboard size={18} /> },
  { to: '/sales',     label: 'Sales',      icon: <TrendingUp size={18} /> },
  { to: '/customers', label: 'Customers',  icon: <Users size={18} /> },
  { to: '/products',  label: 'Products',   icon: <Package size={18} /> },
  { to: '/finance',   label: 'Finance',    icon: <CreditCard size={18} /> },
  { to: '/logistics', label: 'Logistics',  icon: <Truck size={18} /> },
]

/**
 * Adaptive Sidebar — 3 modes: expanded, compact, overlay.
 * Mode is determined by parent App via useAdaptiveNav hook.
 * Props:
 *   mode      — 'expanded' | 'compact' | 'overlay'
 *   isOpen    — boolean (overlay mode drawer state)
 *   onClose   — callback to close overlay
 *   sidebarRef — ref forwarded from parent for focus trapping
 */
export function Sidebar({ mode = 'expanded', isOpen = false, onClose, sidebarRef }) {
  const location = useLocation()
  const firstLinkRef = useRef(null)

  // Close overlay on navigation
  useEffect(() => {
    if (mode === 'overlay' && isOpen && onClose) {
      onClose()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname])

  // Focus trap: focus first link when overlay opens
  useEffect(() => {
    if (mode === 'overlay' && isOpen && firstLinkRef.current) {
      firstLinkRef.current.focus()
    }
  }, [mode, isOpen])

  const sidebarClasses = [
    'sidebar',
    mode === 'overlay' && isOpen ? 'sidebar--open' : '',
  ].filter(Boolean).join(' ')

  return (
    <aside
      ref={sidebarRef}
      className={sidebarClasses}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="sidebar__logo">
        <div className="sidebar__logo-text">Prism Analytics</div>
        <div className="sidebar__logo-sub">Analytics Dashboard</div>
      </div>

      <nav className="sidebar__nav">
        <div className="sidebar__section-label">Dashboards</div>
        {links.map(({ to, label, icon }, idx) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            ref={idx === 0 ? firstLinkRef : undefined}
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            {icon}
            <span className="nav-link__label">{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__footer">
        <div className="status-dot">API Connected</div>
      </div>
    </aside>
  )
}

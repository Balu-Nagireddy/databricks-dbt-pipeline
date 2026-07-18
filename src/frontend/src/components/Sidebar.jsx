import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, TrendingUp, Users, Package,
  CreditCard, Truck, Activity
} from 'lucide-react'

const links = [
  { to: '/',          label: 'Executive',  icon: <LayoutDashboard size={16} /> },
  { to: '/sales',     label: 'Sales',      icon: <TrendingUp size={16} /> },
  { to: '/customers', label: 'Customers',  icon: <Users size={16} /> },
  { to: '/products',  label: 'Products',   icon: <Package size={16} /> },
  { to: '/finance',   label: 'Finance',    icon: <CreditCard size={16} /> },
  { to: '/logistics', label: 'Logistics',  icon: <Truck size={16} /> },
]

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__logo">
        <div className="sidebar__logo-text">Prism Analytics</div>
        <div className="sidebar__logo-sub">Analytics Dashboard</div>
      </div>

      <nav className="sidebar__nav">
        <div className="sidebar__section-label">Dashboards</div>
        {links.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            {icon}
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__footer">
        <div className="status-dot">API Connected</div>
      </div>
    </aside>
  )
}

import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useAdaptiveNav } from './hooks/useAdaptiveNav'
import { Sidebar } from './components/Sidebar'
import { Topbar } from './components/Topbar'
import LandingPage   from './pages/Landing'
import ExecutivePage from './pages/Executive'
import SalesPage     from './pages/Sales'
import CustomersPage from './pages/Customers'
import ProductsPage  from './pages/Products'
import FinancePage   from './pages/Finance'
import LogisticsPage from './pages/Logistics'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
})

/** Inner shell — must be inside BrowserRouter for Sidebar/Topbar to use useLocation */
function AppShell() {
  const { mode, isOpen, setIsOpen, closeOverlay, sidebarRef } = useAdaptiveNav()

  const toggleNav = () => setIsOpen(prev => !prev)

  return (
    <div className="app-shell" data-nav-mode={mode}>
      {/* Skip to main content — accessibility */}
      <a href="#main-content" className="skip-link">Skip to main content</a>

      <Sidebar
        mode={mode}
        isOpen={isOpen}
        onClose={closeOverlay}
        sidebarRef={sidebarRef}
      />

      {/* Overlay backdrop — only rendered in overlay mode */}
      <div
        className={`sidebar-backdrop${isOpen ? ' sidebar-backdrop--visible' : ''}`}
        onClick={() => setIsOpen(false)}
        aria-hidden="true"
      />

      <div className="main-content" id="main-content">
        <Topbar navMode={mode} onToggleNav={toggleNav} />
        <Routes>
          <Route path="/"          element={<ExecutivePage />} />
          <Route path="/sales"     element={<SalesPage />} />
          <Route path="/customers" element={<CustomersPage />} />
          <Route path="/products"  element={<ProductsPage />} />
          <Route path="/finance"   element={<FinancePage />} />
          <Route path="/logistics" element={<LogisticsPage />} />
        </Routes>
      </div>
    </div>
  )
}

export default function App() {
  const [inApp, setInApp] = useState(false)

  if (!inApp) {
    return (
      <QueryClientProvider client={queryClient}>
        <LandingPage onEnter={() => setInApp(true)} />
      </QueryClientProvider>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

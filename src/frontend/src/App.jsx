import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
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
        <div className="app-shell">
          <Sidebar />
          <div className="main-content">
            <Topbar />
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
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}


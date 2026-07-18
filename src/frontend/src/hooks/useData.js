/**
 * TanStack Query hooks — one per API resource.
 * Components call these hooks and never call the API client directly.
 */
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'

const STALE = 60_000 // 1 minute

export const useHealth    = () => useQuery({ queryKey: ['health'],   queryFn: api.health,    staleTime: 30_000 })
export const useVersion   = () => useQuery({ queryKey: ['version'],  queryFn: api.version,   staleTime: Infinity })
export const useKPIs      = () => useQuery({ queryKey: ['kpis'],     queryFn: api.kpis,      staleTime: STALE })

export const useSalesDaily   = (params) => useQuery({ queryKey: ['salesDaily',   params], queryFn: () => api.salesDaily(params),   staleTime: STALE })
export const useSalesMonthly = (params) => useQuery({ queryKey: ['salesMonthly', params], queryFn: () => api.salesMonthly(params), staleTime: STALE })
export const useSalesByState = (params) => useQuery({ queryKey: ['salesByState', params], queryFn: () => api.salesByState(params), staleTime: STALE })

export const useCustomerSegments = (params) => useQuery({ queryKey: ['segments',  params], queryFn: () => api.customerSegments(params), staleTime: STALE })
export const useTopCities        = (params) => useQuery({ queryKey: ['topCities', params], queryFn: () => api.topCities(params),        staleTime: STALE })
export const useRepeatStats      = ()       => useQuery({ queryKey: ['repeatStats'],        queryFn: api.repeatStats,                     staleTime: STALE })

export const useTopProducts  = (params) => useQuery({ queryKey: ['topProducts', params], queryFn: () => api.topProducts(params),  staleTime: STALE })
export const useCategories   = (params) => useQuery({ queryKey: ['categories',  params], queryFn: () => api.categories(params),   staleTime: STALE })

export const usePayments     = () => useQuery({ queryKey: ['payments'],     queryFn: api.payments,     staleTime: STALE })
export const useInstallments = () => useQuery({ queryKey: ['installments'], queryFn: api.installments, staleTime: STALE })

export const useLogisticsPerf  = (params) => useQuery({ queryKey: ['logisticsPerf',  params], queryFn: () => api.logisticsPerf(params),  staleTime: STALE })
export const useSuccessRates   = ()       => useQuery({ queryKey: ['successRates'],             queryFn: api.successRates,                 staleTime: STALE })
export const useSellerShipping = (params) => useQuery({ queryKey: ['sellerShipping', params], queryFn: () => api.sellerShipping(params), staleTime: STALE })

import { AlertTriangle, Inbox } from 'lucide-react'

export function ErrorState({ message = 'Failed to load data.' }) {
  return (
    <div className="error-state">
      <AlertTriangle size={32} />
      <h4>Something went wrong</h4>
      <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>{message}</p>
    </div>
  )
}

export function EmptyState({ message = 'No data available.' }) {
  return (
    <div className="empty-state">
      <Inbox size={40} />
      <h4>No results</h4>
      <p style={{ fontSize: '0.8125rem' }}>{message}</p>
    </div>
  )
}

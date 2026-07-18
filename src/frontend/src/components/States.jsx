import { AlertTriangle, Inbox } from 'lucide-react'

export function ErrorState({ message = 'Failed to load data.' }) {
  return (
    <div className="error-state" role="alert">
      <AlertTriangle size={32} />
      <h4>Something went wrong</h4>
      <p className="error-state__msg">{message}</p>
    </div>
  )
}

export function EmptyState({ message = 'No data available.' }) {
  return (
    <div className="empty-state">
      <Inbox size={40} />
      <h4>No results</h4>
      <p className="empty-state__msg">{message}</p>
    </div>
  )
}

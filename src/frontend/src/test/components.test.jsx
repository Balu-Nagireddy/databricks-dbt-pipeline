import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { KPICard } from '../components/KPICard'
import { ErrorState, EmptyState } from '../components/States'
import { fmt, fmtCurrency, fmtPct, fmtDays, segmentBadge } from '../utils/format'

// ── Format utils ──────────────────────────────────────────────
describe('format utilities', () => {
  it('fmt formats millions', ()  => expect(fmt(1_500_000)).toBe('1.5M'))
  it('fmt formats thousands', () => expect(fmt(3_500)).toBe('3.5K'))
  it('fmt formats small numbers', () => expect(fmt(42)).toBe('42'))
  it('fmt returns dash for null', () => expect(fmt(null)).toBe('—'))
  it('fmtCurrency adds R$', () => expect(fmtCurrency(1_000_000)).toContain('R$'))
  it('fmtPct adds %', () => expect(fmtPct(95.5)).toBe('95.5%'))
  it('fmtDays adds d', () => expect(fmtDays(7.3)).toBe('7.3d'))
  it('segmentBadge maps VIP', () => expect(segmentBadge('VIP')).toBe('badge-indigo'))
  it('segmentBadge maps High Value', () => expect(segmentBadge('High Value')).toBe('badge-teal'))
  it('segmentBadge falls back for unknown', () => expect(segmentBadge('Unknown')).toBe('badge-amber'))
})

// ── KPICard component ─────────────────────────────────────────
describe('KPICard', () => {
  it('renders value and label', () => {
    render(<KPICard value="R$ 5.2M" label="Total Revenue" />)
    expect(screen.getByText('R$ 5.2M')).toBeInTheDocument()
    expect(screen.getByText('Total Revenue')).toBeInTheDocument()
  })

  it('renders skeleton when loading', () => {
    const { container } = render(<KPICard value="R$ 5.2M" label="Revenue" loading />)
    expect(container.querySelector('.skeleton')).toBeInTheDocument()
    expect(screen.queryByText('R$ 5.2M')).not.toBeInTheDocument()
  })
})

// ── State components ──────────────────────────────────────────
describe('ErrorState', () => {
  it('renders default error message', () => {
    render(<ErrorState />)
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })

  it('renders custom message', () => {
    render(<ErrorState message="Database offline." />)
    expect(screen.getByText('Database offline.')).toBeInTheDocument()
  })
})

describe('EmptyState', () => {
  it('renders no results text', () => {
    render(<EmptyState />)
    expect(screen.getByText('No results')).toBeInTheDocument()
  })
})

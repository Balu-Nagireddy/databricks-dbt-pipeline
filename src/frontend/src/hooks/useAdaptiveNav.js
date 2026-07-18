/**
 * useAdaptiveNav — determines sidebar navigation mode based on available viewport space.
 *
 * Modes:
 *   'expanded'  — full sidebar with icons + labels (≥ 1024px)
 *   'compact'   — icons only, hover to expand (640–1023px)
 *   'overlay'   — hidden, hamburger toggle, slide-in drawer (< 640px)
 *
 * Returns { mode, isOpen, setIsOpen, closeOverlay, sidebarRef }
 */
import { useState, useEffect, useRef, useCallback } from 'react'

const EXPANDED_QUERY = '(min-width: 1024px)'
const COMPACT_QUERY  = '(min-width: 640px) and (max-width: 1023.98px)'

function getMode() {
  if (typeof window === 'undefined') return 'expanded'
  if (window.matchMedia(EXPANDED_QUERY).matches) return 'expanded'
  if (window.matchMedia(COMPACT_QUERY).matches)  return 'compact'
  return 'overlay'
}

export function useAdaptiveNav() {
  const [mode, setMode]     = useState(getMode)
  const [isOpen, setIsOpen] = useState(false)
  const sidebarRef          = useRef(null)

  // Listen to viewport changes
  useEffect(() => {
    const mqExpanded = window.matchMedia(EXPANDED_QUERY)
    const mqCompact  = window.matchMedia(COMPACT_QUERY)

    const update = () => {
      const next = getMode()
      setMode(next)
      // Auto-close overlay when switching away from overlay mode
      if (next !== 'overlay') setIsOpen(false)
    }

    mqExpanded.addEventListener('change', update)
    mqCompact.addEventListener('change', update)

    return () => {
      mqExpanded.removeEventListener('change', update)
      mqCompact.removeEventListener('change', update)
    }
  }, [])

  // ESC to close overlay
  useEffect(() => {
    if (mode !== 'overlay' || !isOpen) return

    const onKeyDown = (e) => {
      if (e.key === 'Escape') {
        setIsOpen(false)
      }
    }
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [mode, isOpen])

  // Body scroll lock for overlay
  useEffect(() => {
    if (mode === 'overlay' && isOpen) {
      document.body.style.overflow = 'hidden'
      return () => { document.body.style.overflow = '' }
    }
  }, [mode, isOpen])

  // Close overlay on route navigation (called from Sidebar)
  const closeOverlay = useCallback(() => {
    if (mode === 'overlay') setIsOpen(false)
  }, [mode])

  return { mode, isOpen, setIsOpen, closeOverlay, sidebarRef }
}

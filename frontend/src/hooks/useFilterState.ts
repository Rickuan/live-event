import { useSearchParams } from 'react-router-dom'
import type { EventFilters } from './useEvents'

export function useFilterState(): [EventFilters, (next: Partial<EventFilters>) => void] {
  const [params, setParams] = useSearchParams()

  const filters: EventFilters = {
    city:         params.get('city') ?? undefined,
    genre_id:     params.get('genre_id') ? Number(params.get('genre_id')) : undefined,
    date_from:    params.get('date_from') ?? undefined,
    date_to:      params.get('date_to') ?? undefined,
    include_past: params.get('include_past') === 'true',
  }

  function setFilters(next: Partial<EventFilters>) {
    setParams((prev) => {
      const merged = new URLSearchParams(prev)
      for (const [key, value] of Object.entries(next)) {
        if (value === undefined || value === '' || value === false) {
          merged.delete(key)
        } else {
          merged.set(key, String(value))
        }
      }
      return merged
    }, { replace: true })
  }

  return [filters, setFilters]
}

import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/axios'
import type { EventListResponse } from '../types/api'

export interface EventFilters {
  city?: string
  genre_id?: number
  date_from?: string   // YYYY-MM-DD
  date_to?: string     // YYYY-MM-DD
  include_past?: boolean
}

export function useEvents(filters: EventFilters = {}) {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== '' && v !== false),
  )

  return useQuery<EventListResponse>({
    queryKey: ['events', params],
    queryFn: () => api.get('/events', { params }).then((r) => r.data),
  })
}

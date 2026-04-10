import { useQuery } from '@tanstack/react-query'
import { api } from '../../lib/axios'
import type { GenreListResponse, CityListResponse } from '../../types/api'
import type { EventFilters } from '../../hooks/useEvents'

interface Props {
  filters: EventFilters
  onChange: (next: Partial<EventFilters>) => void
}

const inputClass =
  'text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white focus:outline-none focus:ring-2 focus:ring-gray-200 text-gray-700'

export default function FilterBar({ filters, onChange }: Props) {
  const { data: genres } = useQuery<GenreListResponse>({
    queryKey: ['genres'],
    queryFn: () => api.get('/genres').then((r) => ({ items: r.data })),
  })

  const { data: cities } = useQuery<CityListResponse>({
    queryKey: ['cities'],
    queryFn: () => api.get('/venues/cities').then((r) => ({ cities: r.data })),
  })

  return (
    <div className="flex flex-wrap gap-2 items-center">
      {/* City */}
      <select
        value={filters.city ?? ''}
        onChange={(e) => onChange({ city: e.target.value || undefined })}
        className={inputClass}
      >
        <option value="">所有城市</option>
        {cities?.cities.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      {/* Genre */}
      <select
        value={filters.genre_id ?? ''}
        onChange={(e) => onChange({ genre_id: e.target.value ? Number(e.target.value) : undefined })}
        className={inputClass}
      >
        <option value="">所有類型</option>
        {genres?.items.map((g) => (
          <option key={g.id} value={g.id}>{g.name}</option>
        ))}
      </select>

      {/* Date from */}
      <input
        type="date"
        value={filters.date_from ?? ''}
        onChange={(e) => onChange({ date_from: e.target.value || undefined })}
        className={inputClass}
      />

      {/* Date to */}
      <input
        type="date"
        value={filters.date_to ?? ''}
        onChange={(e) => onChange({ date_to: e.target.value || undefined })}
        className={inputClass}
      />

      {/* Include past */}
      <label className="flex items-center gap-1.5 text-sm text-gray-600 cursor-pointer select-none">
        <input
          type="checkbox"
          checked={filters.include_past ?? false}
          onChange={(e) => onChange({ include_past: e.target.checked || undefined })}
          className="rounded border-gray-300"
        />
        顯示過去活動
      </label>
    </div>
  )
}

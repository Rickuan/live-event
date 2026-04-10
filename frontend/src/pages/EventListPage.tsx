import { useEvents } from '../hooks/useEvents'
import { useFilterState } from '../hooks/useFilterState'
import FilterBar from '../components/events/FilterBar'
import EventGrid from '../components/events/EventGrid'
import EmptyState from '../components/events/EmptyState'

export default function EventListPage() {
  const [filters, setFilters] = useFilterState()
  const { data, isLoading, isError } = useEvents(filters)

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <FilterBar filters={filters} onChange={setFilters} />

      {isLoading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="rounded-2xl bg-zinc-100 animate-pulse h-[180px]" />
          ))}
        </div>
      )}

      {isError && (
        <p className="text-sm text-red-400">無法載入活動，請稍後再試</p>
      )}

      {!isLoading && !isError && (
        <>
          {data && data.total > 0 ? (
            <>
              <p className="text-xs text-gray-400">{data.total} 場活動</p>
              <EventGrid events={data.items} />
            </>
          ) : (
            <EmptyState />
          )}
        </>
      )}
    </div>
  )
}

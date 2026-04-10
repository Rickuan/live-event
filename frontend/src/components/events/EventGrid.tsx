import type { Event } from '../../types'
import EventCard from './EventCard'

interface Props {
  events: Event[]
}

export default function EventGrid({ events }: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  )
}

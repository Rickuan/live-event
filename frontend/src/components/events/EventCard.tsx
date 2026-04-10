import { clsx } from 'clsx'
import type { Event } from '../../types'
import PriceBadge from './PriceBadge'

interface Props {
  event: Event
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('zh-TW', {
    timeZone: 'Asia/Taipei',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short',
  })
}

export default function EventCard({ event }: Props) {
  const isPast = new Date(event.start_at) < new Date()
  const href = event.ticket_url ?? event.info_url ?? '#'

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={clsx(
        'group block rounded-2xl overflow-hidden transition-transform hover:-translate-y-0.5',
        isPast && 'grayscale opacity-60',
      )}
    >
      {/* Card body */}
      <div className="bg-zinc-800 p-5 h-full flex flex-col gap-3 min-h-[180px]">
        {/* Venue */}
        <p className="text-xs text-zinc-400 truncate">
          {event.venue.city} · {event.venue.name}
        </p>

        {/* Title */}
        <h3 className="text-white font-semibold text-base leading-snug line-clamp-2 flex-1">
          {event.title}
        </h3>

        {/* Artists */}
        {event.artists.length > 0 && (
          <p className="text-zinc-400 text-xs truncate">
            {event.artists.map((a) => a.name).join('、')}
          </p>
        )}

        {/* Footer: date + price */}
        <div className="flex items-center justify-between gap-2 mt-auto pt-2 border-t border-white/10">
          <span className="text-zinc-400 text-xs whitespace-nowrap">
            {formatDate(event.start_at)}
          </span>
          <PriceBadge
            priceType={event.price_type}
            minPrice={event.min_price}
            maxPrice={event.max_price}
          />
        </div>

        {/* Cancelled badge */}
        {event.is_cancelled && (
          <span className="text-xs text-red-400 font-medium">已取消</span>
        )}
      </div>
    </a>
  )
}

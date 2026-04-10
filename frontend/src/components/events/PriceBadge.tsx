import type { PriceType } from '../../types'

interface Props {
  priceType: PriceType
  minPrice: number | null
  maxPrice: number | null
}

function formatPrice(min: number | null, max: number | null): string {
  if (min === null) return ''
  if (max === null || max === min) return `NT$${min.toLocaleString()}`
  return `NT$${min.toLocaleString()} ~ ${max.toLocaleString()}`
}

const STYLES: Record<PriceType, string> = {
  free:     'bg-emerald-100 text-emerald-700',
  donation: 'bg-amber-100 text-amber-700',
  paid:     'bg-white/20 text-white',
  tbd:      'bg-white/10 text-white/60',
}

const LABELS: Record<PriceType, string> = {
  free:     '免費',
  donation: '樂捐',
  paid:     '',
  tbd:      '票價待確認',
}

export default function PriceBadge({ priceType, minPrice, maxPrice }: Props) {
  const label = priceType === 'paid' ? formatPrice(minPrice, maxPrice) : LABELS[priceType]

  return (
    <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full ${STYLES[priceType]}`}>
      {label}
    </span>
  )
}

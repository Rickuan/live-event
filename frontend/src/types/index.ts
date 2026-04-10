export type PriceType = 'paid' | 'free' | 'donation' | 'tbd'

export interface Genre {
  id: number
  name: string
}

export interface Venue {
  id: number
  name: string
  address: string
  city: string
}

export interface Artist {
  id: number
  name: string
  genre: Genre | null
}

export interface Event {
  id: number
  title: string
  start_at: string        // ISO 8601
  end_at: string | null
  min_price: number | null
  max_price: number | null
  price_type: PriceType
  ticket_url: string | null
  info_url: string | null
  venue: Venue
  artists: Artist[]
  is_cancelled: boolean
  is_sold_out: boolean
  is_hidden: boolean
  provider: string
  scraped_at: string
}

export interface EventDetail extends Event { }

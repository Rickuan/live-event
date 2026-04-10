import type { Event, EventDetail, Genre } from './index'

export interface EventListResponse {
  items: Event[]
  total: number
}

export interface EventDetailResponse {
  item: EventDetail
}

export interface AdminHealthResponse {
  provider: string
  run_at: string | null       // ISO 8601，null 代表從未執行
  events_count: number | null
  has_warning: boolean
}

export interface AdminLoginResponse {
  access_token: string
  token_type: 'bearer'
}

export interface GenreListResponse {
  items: Genre[]
}

export interface CityListResponse {
  cities: string[]
}

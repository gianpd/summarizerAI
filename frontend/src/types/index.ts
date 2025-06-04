export interface Summary {
  id: number
  url: string
  summary?: string
  key_top?: string  // This is the title from backend
  keywords?: string
  created_at: string
  updated_at?: string
}

export interface SummaryCreate {
  url: string
}

export interface SummaryResponse {
  id: number
  url?: string
  summary?: string
  key_top?: string  // This is the title from backend
  keywords?: string
  created_at: string
  updated_at?: string
}

export interface ApiError {
  detail: string
}

export interface HealthCheck {
  status: string
  timestamp: string
}
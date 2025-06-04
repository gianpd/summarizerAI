export interface Summary {
  id: number
  title: string
  content: string
  summary: string
  url?: string
  created_at: string
  updated_at: string
}

export interface SummaryCreate {
  title: string
  content?: string
  url?: string
}

export interface SummaryResponse {
  id: number
  title?: string
  content?: string
  summary?: string
  url?: string
  created_at: string
  updated_at: string
}

export interface ApiError {
  detail: string
}

export interface HealthCheck {
  status: string
  timestamp: string
}
// types/index.ts - Centralized type exports

// User types
export interface User {
  id: number
  first_name: string
  last_name: string
  email: string
  location: string
  flatmate_pref: string[]
  keywords: string[]
  role: 'seeker' | 'renter' | 'admin'
  created_at: string
}

export interface UserData {
  first_name: string
  last_name: string
  email: string
  password: string
  location: string
  flatmate_pref?: string[]
  keywords?: string[]
  role?: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface TokenRefreshResponse {
  access_token: string
  token_type: string
}

// Apartment types
export type ApartmentStatus = 'draft' | 'published' | 'archived'
export type ApartmentType = 'studio' | '1bhk' | '2bhk' | '3bhk' | '4bhk' | 'villa' | 'penthouse'
export type FurnishingType = 'furnished' | 'semi-furnished' | 'unfurnished'
export type ParkingType = 'none' | 'street' | 'garage' | 'covered'
export type GenderPreference = 'any' | 'male' | 'female'

export interface Apartment {
  id: number
  title: string
  description: string
  location: string
  apartment_type: string
  rent_per_week: number
  start_date: string
  duration_len: number | null
  place_accept: string
  furnishing_type: string
  is_bathroom_solo: boolean
  parking_type: string
  keywords: string[]
  is_active: boolean
  status: ApartmentStatus
  images: string[]
  renter_id: number
  view_count: number
  is_featured: boolean
  featured_until: string | null
  featured_priority: number
  created_at: string
  updated_at: string
  renter?: User
}

export interface ApartmentCreate {
  title: string
  description: string
  location: string
  apartment_type: string
  rent_per_week: number
  start_date: string
  duration_len?: number | null
  place_accept: string
  furnishing_type: string
  is_bathroom_solo: boolean
  parking_type: string
  keywords: string[]
  is_active?: boolean
  status?: ApartmentStatus
}

export interface ApartmentFilters {
  location?: string
  apartment_type?: string
  min_price?: number
  max_price?: number
  start_date_from?: string
  start_date_to?: string
  duration_min?: number
  duration_max?: number
  furnishing_type?: string
  is_bathroom_solo?: boolean
  parking_type?: string
  place_accept?: string
  keywords?: string[]
  is_active?: boolean
  status?: ApartmentStatus
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pages: number
  size: number
}

// Message types
export interface Message {
  id: number
  sender_id: number
  receiver_id: number
  apartment_id: number | null
  content: string
  is_read: boolean
  read_at: string | null
  created_at: string
  updated_at: string
  sender?: User
  receiver?: User
  apartment?: Apartment
}

export interface Conversation {
  other_user: User
  last_message: Message
  unread_count: number
  apartment?: Apartment
}

export interface SendMessageData {
  receiver_id: number
  content: string
  apartment_id?: number
}

// Notification types
export type NotificationType = 'message' | 'inquiry' | 'system' | 'apartment'

export interface Notification {
  id: number
  user_id: number
  title: string
  content: string
  type: NotificationType
  is_read: boolean
  data: Record<string, any>
  created_at: string
}

// Search types
export interface SearchResult {
  apartments: Apartment[]
  total: number
  suggestions?: string[]
}

export interface AutocompleteResult {
  suggestions: string[]
  field: string
}

// Admin types
export interface PlatformStats {
  total_users: number
  total_apartments: number
  active_apartments: number
  total_messages: number
  users_by_role: {
    seeker: number
    renter: number
    admin: number
  }
  apartments_by_status: {
    draft: number
    published: number
    archived: number
  }
}

// API Error
export interface ApiError {
  detail: string | { msg: string; loc: string[] }[]
  status_code?: number
}

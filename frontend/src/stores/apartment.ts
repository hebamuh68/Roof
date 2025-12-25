// stores/apartment.ts - Apartment store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Apartment, ApartmentCreate, ApartmentFilters, PaginatedResponse } from '@/types'
import api from '@/services/api'

export const useApartmentStore = defineStore('apartment', () => {
  // State
  const apartments = ref<Apartment[]>([])
  const currentApartment = ref<Apartment | null>(null)
  const myApartments = ref<Apartment[]>([])
  const featuredApartments = ref<Apartment[]>([])
  const popularApartments = ref<Apartment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    total: 0,
    page: 1,
    pages: 1,
    size: 12
  })

  // Getters
  const hasApartments = computed(() => apartments.value.length > 0)
  const publishedApartments = computed(() =>
    apartments.value.filter((a) => a.status === 'published' && a.is_active)
  )

  // Fetch all apartments (backend uses skip/limit pagination)
  const fetchApartments = async (
    page = 1,
    size = 12,
    filters?: ApartmentFilters,
    showFeaturedFirst = true
  ): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const skip = (page - 1) * size
      const params = new URLSearchParams({
        skip: skip.toString(),
        limit: size.toString(),
        show_featured_first: showFeaturedFirst.toString()
      })

      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== '') {
            if (Array.isArray(value)) {
              value.forEach((v) => params.append(key, v))
            } else {
              params.append(key, value.toString())
            }
          }
        })
      }

      const response = await api.get<PaginatedResponse<Apartment>>(`/apartments?${params}`)
      apartments.value = response.data.apartments || response.data.items || response.data
      pagination.value = {
        total: response.data.total || apartments.value.length,
        page: page,
        pages: Math.ceil((response.data.total || apartments.value.length) / size),
        size: size
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch apartments'
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch single apartment (with view tracking)
  const fetchApartment = async (id: number, trackView = true): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await api.get<Apartment>(`/apartments/${id}?track_view=${trackView}`)
      currentApartment.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch apartment'
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch my apartments
  const fetchMyApartments = async (status?: string, skip = 0, limit = 100): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams({
        skip: skip.toString(),
        limit: limit.toString()
      })
      if (status) params.append('status', status)

      const response = await api.get(`/apartments/my-apartments?${params}`)
      myApartments.value = response.data.apartments || response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch your apartments'
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch my apartments analytics
  const fetchMyApartmentsAnalytics = async (): Promise<any> => {
    try {
      const response = await api.get('/apartments/my-apartments/analytics')
      return response.data
    } catch (err) {
      return null
    }
  }

  // Fetch featured apartments
  const fetchFeaturedApartments = async (): Promise<boolean> => {
    try {
      const response = await api.get<Apartment[]>('/apartments/featured/list')
      featuredApartments.value = response.data
      return true
    } catch (err: any) {
      return false
    }
  }

  // Fetch popular apartments
  const fetchPopularApartments = async (limit = 10): Promise<boolean> => {
    try {
      const response = await api.get<Apartment[]>(`/apartments/popular/list?limit=${limit}`)
      popularApartments.value = response.data
      return true
    } catch (err: any) {
      return false
    }
  }

  // Create apartment
  const createApartment = async (
    data: ApartmentCreate,
    images: File[]
  ): Promise<Apartment | null> => {
    loading.value = true
    error.value = null

    try {
      const formData = new FormData()

      // Append apartment data
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          if (Array.isArray(value)) {
            value.forEach((v) => formData.append(key, v))
          } else if (typeof value === 'boolean') {
            formData.append(key, value.toString())
          } else {
            formData.append(key, value.toString())
          }
        }
      })

      // Append images
      images.forEach((image) => {
        formData.append('images', image)
      })

      const response = await api.post<Apartment>('/apartments', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      myApartments.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create apartment'
      return null
    } finally {
      loading.value = false
    }
  }

  // Update apartment
  const updateApartment = async (
    id: number,
    data: Partial<ApartmentCreate>,
    newImages?: File[]
  ): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const formData = new FormData()

      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          if (Array.isArray(value)) {
            value.forEach((v) => formData.append(key, v))
          } else if (typeof value === 'boolean') {
            formData.append(key, value.toString())
          } else {
            formData.append(key, value.toString())
          }
        }
      })

      if (newImages) {
        newImages.forEach((image) => {
          formData.append('images', image)
        })
      }

      const response = await api.put<Apartment>(`/apartments/${id}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      // Update in lists
      const index = myApartments.value.findIndex((a) => a.id === id)
      if (index !== -1) myApartments.value[index] = response.data
      if (currentApartment.value?.id === id) currentApartment.value = response.data

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update apartment'
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete apartment
  const deleteApartment = async (id: number): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      await api.delete(`/apartments/${id}`)
      myApartments.value = myApartments.value.filter((a) => a.id !== id)
      apartments.value = apartments.value.filter((a) => a.id !== id)
      if (currentApartment.value?.id === id) currentApartment.value = null
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete apartment'
      return false
    } finally {
      loading.value = false
    }
  }

  // Publish apartment
  const publishApartment = async (id: number): Promise<boolean> => {
    try {
      const response = await api.post<Apartment>(`/apartments/${id}/publish`)
      const index = myApartments.value.findIndex((a) => a.id === id)
      if (index !== -1) myApartments.value[index] = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to publish apartment'
      return false
    }
  }

  // Archive apartment
  const archiveApartment = async (id: number): Promise<boolean> => {
    try {
      const response = await api.post<Apartment>(`/apartments/${id}/archive`)
      const index = myApartments.value.findIndex((a) => a.id === id)
      if (index !== -1) myApartments.value[index] = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to archive apartment'
      return false
    }
  }

  // Duplicate apartment
  const duplicateApartment = async (id: number): Promise<Apartment | null> => {
    try {
      const response = await api.post<Apartment>(`/apartments/${id}/duplicate`)
      myApartments.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to duplicate apartment'
      return null
    }
  }

  // Feature apartment
  const featureApartment = async (id: number, durationDays = 7, priority = 1): Promise<boolean> => {
    try {
      const response = await api.post<Apartment>(`/apartments/${id}/feature`, {
        duration_days: durationDays,
        priority: priority
      })
      const index = myApartments.value.findIndex((a) => a.id === id)
      if (index !== -1) myApartments.value[index] = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to feature apartment'
      return false
    }
  }

  // Unfeature apartment
  const unfeatureApartment = async (id: number): Promise<boolean> => {
    try {
      const response = await api.delete<Apartment>(`/apartments/${id}/feature`)
      const index = myApartments.value.findIndex((a) => a.id === id)
      if (index !== -1) myApartments.value[index] = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to unfeature apartment'
      return false
    }
  }

  // Bulk operations
  const bulkOperation = async (
    apartmentIds: number[],
    action: 'PUBLISH' | 'ARCHIVE' | 'DELETE' | 'ACTIVATE' | 'DEACTIVATE' | 'FEATURE' | 'UNFEATURE',
    featureDays?: number
  ): Promise<{ succeeded: number[]; failed: number[] } | null> => {
    try {
      const payload: any = {
        apartment_ids: apartmentIds,
        action: action
      }
      if (featureDays) payload.feature_days = featureDays

      const response = await api.post('/apartments/bulk-operation', payload)
      await fetchMyApartments()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Bulk operation failed'
      return null
    }
  }

  // Clear current apartment
  const clearCurrentApartment = () => {
    currentApartment.value = null
  }

  return {
    // State
    apartments,
    currentApartment,
    myApartments,
    featuredApartments,
    popularApartments,
    loading,
    error,
    pagination,
    // Getters
    hasApartments,
    publishedApartments,
    // Actions
    fetchApartments,
    fetchApartment,
    fetchMyApartments,
    fetchMyApartmentsAnalytics,
    fetchFeaturedApartments,
    fetchPopularApartments,
    createApartment,
    updateApartment,
    deleteApartment,
    publishApartment,
    archiveApartment,
    duplicateApartment,
    featureApartment,
    unfeatureApartment,
    bulkOperation,
    clearCurrentApartment
  }
})

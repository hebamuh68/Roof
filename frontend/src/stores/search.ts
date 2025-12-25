// stores/search.ts - Search and filter store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Apartment, ApartmentFilters } from '@/types'
import api from '@/services/api'

export const useSearchStore = defineStore('search', () => {
  // State
  const searchQuery = ref('')
  const searchResults = ref<Apartment[]>([])
  const suggestions = ref<string[]>([])
  const spellingSuggestions = ref<string[]>([])
  const filters = ref<ApartmentFilters>({})
  const loading = ref(false)
  const error = ref<string | null>(null)
  const totalResults = ref(0)

  // Active filters count
  const activeFiltersCount = computed(() => {
    return Object.entries(filters.value).filter(([_, value]) => {
      if (Array.isArray(value)) return value.length > 0
      return value !== undefined && value !== null && value !== ''
    }).length
  })

  // Search apartments (backend uses skip/limit and query parameter)
  const search = async (
    query: string,
    skip = 0,
    limit = 12,
    sortBy = 'relevance',
    fuzziness = 'AUTO'
  ): Promise<boolean> => {
    loading.value = true
    error.value = null
    searchQuery.value = query

    try {
      const params = new URLSearchParams({
        query: query,
        skip: skip.toString(),
        limit: limit.toString(),
        sort_by: sortBy,
        fuzziness: fuzziness
      })
      const response = await api.get(`/search/apartments?${params}`)
      searchResults.value = response.data || []
      totalResults.value = Array.isArray(response.data) ? response.data.length : 0
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Search failed'
      return false
    } finally {
      loading.value = false
    }
  }

  // Filter apartments (POST endpoint)
  const filterApartments = async (filterData: ApartmentFilters): Promise<boolean> => {
    loading.value = true
    error.value = null
    filters.value = filterData

    try {
      const response = await api.post('/filter/apartments', filterData)
      searchResults.value = response.data || []
      totalResults.value = Array.isArray(response.data) ? response.data.length : 0
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Filter failed'
      return false
    } finally {
      loading.value = false
    }
  }

  // Get autocomplete suggestions
  const getAutocompleteSuggestions = async (
    query: string,
    field: 'all' | 'title' | 'location' | 'keywords' = 'all',
    limit = 10
  ): Promise<string[]> => {
    if (!query || query.length < 2) {
      suggestions.value = []
      return []
    }

    try {
      const params = new URLSearchParams({
        query: query,
        field: field,
        limit: limit.toString()
      })
      const response = await api.get(`/autocomplete?${params}`)
      suggestions.value = response.data?.suggestions || response.data || []
      return suggestions.value
    } catch (err) {
      suggestions.value = []
      return []
    }
  }

  // Get spelling suggestions
  const getSpellingSuggestions = async (query: string): Promise<string[]> => {
    if (!query || query.length < 3) {
      spellingSuggestions.value = []
      return []
    }

    try {
      const response = await api.get(`/search/suggestions?query=${encodeURIComponent(query)}`)
      spellingSuggestions.value = response.data?.suggestions || response.data || []
      return spellingSuggestions.value
    } catch (err) {
      spellingSuggestions.value = []
      return []
    }
  }

  // Clear filters
  const clearFilters = () => {
    filters.value = {}
  }

  // Clear search
  const clearSearch = () => {
    searchQuery.value = ''
    searchResults.value = []
    suggestions.value = []
    spellingSuggestions.value = []
    totalResults.value = 0
  }

  // Set single filter
  const setFilter = <K extends keyof ApartmentFilters>(key: K, value: ApartmentFilters[K]) => {
    filters.value[key] = value
  }

  // Remove single filter
  const removeFilter = (key: keyof ApartmentFilters) => {
    delete filters.value[key]
  }

  return {
    // State
    searchQuery,
    searchResults,
    suggestions,
    spellingSuggestions,
    filters,
    loading,
    error,
    totalResults,
    // Getters
    activeFiltersCount,
    // Actions
    search,
    filterApartments,
    getAutocompleteSuggestions,
    getSpellingSuggestions,
    clearFilters,
    clearSearch,
    setFilter,
    removeFilter
  }
})

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute top-20 w-72 h-72 rounded-full blur-3xl opacity-10 orb-start" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute bottom-20 w-72 h-72 rounded-full blur-3xl opacity-10 orb-end" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-heading-1 text-white mb-2">{{ $t('apartments.browse') }}</h1>
        <p class="text-body text-gray-400">{{ $t('apartments.subtitle') }}</p>
      </div>

      <!-- Search and Filters Bar -->
      <div class="flex flex-col sm:flex-row gap-4 mb-8">
        <!-- Search Input -->
        <div class="flex-1 relative">
          <input
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            type="text"
            :placeholder="$t('apartments.searchPlaceholder')"
            class="w-full px-4 py-3 pl-12 bg-white bg-opacity-10 backdrop-blur-sm border border-white border-opacity-20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 focus:border-transparent transition-all"
          />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <button
            v-if="searchQuery"
            @click="clearSearch"
            class="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-white hover:bg-opacity-10 rounded-full transition-colors"
          >
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Filter Panel -->
        <FilterPanel
          v-model="filters"
          :loading="loading"
          @apply="applyFilters"
          @clear="clearFilters"
        />

        <!-- Sort Dropdown -->
        <select
          v-model="sortBy"
          @change="handleSort"
          class="px-4 py-3 bg-white bg-opacity-10 backdrop-blur-sm border border-white border-opacity-20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 cursor-pointer"
        >
          <option value="relevance" class="bg-gray-800">{{ $t('apartments.sort.relevance') }}</option>
          <option value="price_asc" class="bg-gray-800">{{ $t('apartments.sort.priceAsc') }}</option>
          <option value="price_desc" class="bg-gray-800">{{ $t('apartments.sort.priceDesc') }}</option>
          <option value="date_desc" class="bg-gray-800">{{ $t('apartments.sort.dateDesc') }}</option>
          <option value="views_desc" class="bg-gray-800">{{ $t('apartments.sort.viewsDesc') }}</option>
        </select>
      </div>

      <!-- Active Filters -->
      <div v-if="activeFilterTags.length > 0" class="flex flex-wrap gap-2 mb-6">
        <span
          v-for="tag in activeFilterTags"
          :key="tag.key"
          class="inline-flex items-center gap-1 px-3 py-1 bg-secondary-500 bg-opacity-20 text-secondary-300 rounded-full text-sm"
        >
          {{ tag.label }}
          <button @click="removeFilter(tag.key)" class="hover:text-white transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </span>
        <button
          @click="clearAllFilters"
          class="text-sm text-gray-400 hover:text-white transition-colors"
        >
          {{ $t('apartments.filters.clearAll') }}
        </button>
      </div>

      <!-- Results Count -->
      <div class="flex items-center justify-between mb-6">
        <p class="text-gray-400">
          <span v-if="loading">{{ $t('apartments.loading') }}</span>
          <span v-else>{{ totalResults }} {{ $t('apartments.found') }}</span>
        </p>
      </div>

      <!-- Apartments Grid -->
      <ApartmentGrid
        :apartments="apartments"
        :loading="loading"
        :empty-message="$t('apartments.noResults')"
        @select="viewApartment"
      />

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center mt-10">
        <div class="flex items-center gap-2">
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="p-2 rounded-lg bg-white bg-opacity-10 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-opacity-20 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>

          <template v-for="page in visiblePages" :key="page">
            <button
              v-if="page !== '...'"
              @click="goToPage(page as number)"
              :class="[
                'w-10 h-10 rounded-lg font-medium transition-all',
                currentPage === page
                  ? 'text-white shadow-lg'
                  : 'bg-white bg-opacity-10 text-gray-300 hover:bg-opacity-20'
              ]"
              :style="currentPage === page ? { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' } : {}"
            >
              {{ page }}
            </button>
            <span v-else class="px-2 text-gray-500">...</span>
          </template>

          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="p-2 rounded-lg bg-white bg-opacity-10 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-opacity-20 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
import { useRouter, useRoute } from 'vue-router'
import { useApartmentStore } from '@/stores/apartment'
import type { Apartment, ApartmentFilters } from '@/types'
import ApartmentGrid from '@/components/apartments/ApartmentGrid.vue'
import FilterPanel from '@/components/apartments/FilterPanel.vue'

const router = useRouter()
const route = useRoute()
const apartmentStore = useApartmentStore()

const searchQuery = ref('')
const filters = ref<ApartmentFilters>({})
const sortBy = ref('relevance')
const currentPage = ref(1)
const pageSize = 12

const apartments = computed(() => apartmentStore.apartments)
const loading = computed(() => apartmentStore.loading)
const totalResults = computed(() => apartmentStore.pagination.total)
const totalPages = computed(() => apartmentStore.pagination.pages)


const activeFilterTags = computed(() => {
  const tags: { key: string; label: string }[] = []
  const f = filters.value

  if (f.location) tags.push({ key: 'location', label: `${t('putAnAd.location')}: ${f.location}` })
  if (f.apartment_type) tags.push({ key: 'apartment_type', label: f.apartment_type.toUpperCase() })
  if (f.min_price || f.max_price) {
    const priceLabel = f.min_price && f.max_price
      ? `${f.min_price.toLocaleString()} - ${f.max_price.toLocaleString()} EGP`
      : f.min_price
        ? `${t('common.from')} ${f.min_price.toLocaleString()} EGP`
        : `${t('common.upTo')} ${f.max_price?.toLocaleString()} EGP`
    tags.push({ key: 'price', label: priceLabel })
  }
  if (f.furnishing_type) tags.push({ key: 'furnishing_type', label: f.furnishing_type })
  if (f.parking_type) tags.push({ key: 'parking_type', label: `${t('common.parking')}: ${f.parking_type}` })
  if (f.is_bathroom_solo !== undefined) {
    tags.push({ key: 'is_bathroom_solo', label: f.is_bathroom_solo ? t('common.privateBathroom') : t('common.sharedBathroom') })
  }

  return tags
})

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const total = totalPages.value
  const current = currentPage.value

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i)
    }
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }

  return pages
})

const fetchApartments = async () => {
  await apartmentStore.fetchApartments(currentPage.value, pageSize, {
    ...filters.value,
    is_active: true,
    status: 'published'
  })
}

const handleSearch = async () => {
  if (searchQuery.value.trim()) {
    router.push({ name: 'search', query: { q: searchQuery.value } })
  }
}

const clearSearch = () => {
  searchQuery.value = ''
}

const applyFilters = () => {
  currentPage.value = 1
  fetchApartments()
}

const clearFilters = () => {
  filters.value = {}
  currentPage.value = 1
  fetchApartments()
}

const removeFilter = (key: string) => {
  if (key === 'price') {
    delete filters.value.min_price
    delete filters.value.max_price
  } else {
    delete filters.value[key as keyof ApartmentFilters]
  }
  fetchApartments()
}

const clearAllFilters = () => {
  filters.value = {}
  fetchApartments()
}

const handleSort = () => {
  // Sorting is typically handled by the backend
  // For now, we'll refetch with sort parameter
  fetchApartments()
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchApartments()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const viewApartment = (apartment: Apartment) => {
  router.push({ name: 'apartmentDetail', params: { id: apartment.id } })
}

// Initialize from URL query params
onMounted(() => {
  const query = route.query
  if (query.location) filters.value.location = query.location as string
  if (query.type) filters.value.apartment_type = query.type as string

  fetchApartments()
})

watch(() => route.query, () => {
  const query = route.query
  if (query.location) filters.value.location = query.location as string
  if (query.type) filters.value.apartment_type = query.type as string
  fetchApartments()
})
</script>

<style scoped>
.orb-start {
  left: -5rem;
}

.orb-end {
  right: -5rem;
}

[dir="rtl"] .orb-start {
  left: auto;
  right: -5rem;
}

[dir="rtl"] .orb-end {
  right: auto;
  left: -5rem;
}
</style>

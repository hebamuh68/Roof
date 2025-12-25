<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Search Header -->
      <div class="mb-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-white mb-4">{{ $t('common.searchResults') }}</h1>

        <!-- Search Bar -->
        <div class="relative max-w-2xl">
          <input
            v-model="searchQuery"
            @input="handleSearchInput"
            @keyup.enter="performSearch"
            type="text"
            :placeholder="$t('apartments.searchPlaceholder')"
            class="w-full px-5 py-4 pl-12 bg-white bg-opacity-10 backdrop-blur-sm border border-white border-opacity-20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 text-lg"
          />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>

          <!-- Autocomplete Dropdown -->
          <div
            v-if="showSuggestions && (suggestions.length > 0 || spellingSuggestions.length > 0)"
            class="absolute top-full left-0 right-0 mt-2 bg-gray-800 rounded-xl border border-gray-700 shadow-xl overflow-hidden z-10"
          >
            <!-- Spelling Suggestions -->
            <div v-if="spellingSuggestions.length > 0" class="p-3 border-b border-gray-700">
              <p class="text-sm text-gray-400 mb-2">Did you mean:</p>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="suggestion in spellingSuggestions"
                  :key="suggestion"
                  @click="useSpellingSuggestion(suggestion)"
                  class="px-3 py-1 bg-secondary-500 bg-opacity-20 text-secondary-300 rounded-lg text-sm hover:bg-opacity-30 transition-colors"
                >
                  {{ suggestion }}
                </button>
              </div>
            </div>

            <!-- Autocomplete Suggestions -->
            <div v-if="suggestions.length > 0">
              <button
                v-for="suggestion in suggestions"
                :key="suggestion"
                @click="useSuggestion(suggestion)"
                class="w-full px-4 py-3 text-left text-white hover:bg-gray-700 transition-colors flex items-center gap-3"
              >
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                {{ suggestion }}
              </button>
            </div>
          </div>
        </div>

        <!-- Results Count -->
        <p v-if="!loading && searchQuery" class="text-gray-400 mt-4">
          {{ totalResults }} {{ $t('common.resultsFor') }} "{{ searchQuery }}"
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div v-for="i in 8" :key="i" class="bg-white rounded-2xl shadow-md overflow-hidden animate-pulse">
          <div class="h-48 bg-gray-200"></div>
          <div class="p-4 space-y-3">
            <div class="h-5 bg-gray-200 rounded w-3/4"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="searchResults.length === 0 && searchQuery" class="text-center py-16">
        <svg class="w-20 h-20 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <h3 class="text-xl font-medium text-white mb-2">{{ $t('common.noResultsFound') }}</h3>
        <p class="text-gray-400 mb-6">{{ $t('common.tryDifferentKeywords') }}</p>
      </div>

      <!-- Results Grid -->
      <ApartmentGrid
        v-else
        :apartments="searchResults"
        :loading="loading"
        @select="viewApartment"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useSearchStore } from '@/stores/search'
import type { Apartment } from '@/types'
import ApartmentGrid from '@/components/apartments/ApartmentGrid.vue'

const { t } = useI18n()

const route = useRoute()
const router = useRouter()
const searchStore = useSearchStore()

const searchQuery = ref('')
const showSuggestions = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

const searchResults = computed(() => searchStore.searchResults)
const suggestions = computed(() => searchStore.suggestions)
const spellingSuggestions = computed(() => searchStore.spellingSuggestions)
const loading = computed(() => searchStore.loading)
const totalResults = computed(() => searchStore.totalResults)

const handleSearchInput = () => {
  if (debounceTimer) clearTimeout(debounceTimer)

  debounceTimer = setTimeout(async () => {
    if (searchQuery.value.length >= 2) {
      await searchStore.getAutocompleteSuggestions(searchQuery.value)
      await searchStore.getSpellingSuggestions(searchQuery.value)
      showSuggestions.value = true
    } else {
      showSuggestions.value = false
    }
  }, 300)
}

const performSearch = async () => {
  showSuggestions.value = false
  if (searchQuery.value.trim()) {
    router.replace({ query: { q: searchQuery.value } })
    await searchStore.search(searchQuery.value)
  }
}

const useSuggestion = (suggestion: string) => {
  searchQuery.value = suggestion
  showSuggestions.value = false
  performSearch()
}

const useSpellingSuggestion = (suggestion: string) => {
  searchQuery.value = suggestion
  showSuggestions.value = false
  performSearch()
}

const viewApartment = (apartment: Apartment) => {
  router.push({ name: 'apartmentDetail', params: { id: apartment.id } })
}

// Close suggestions on click outside
const handleClickOutside = () => {
  showSuggestions.value = false
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)

  const query = route.query.q as string
  if (query) {
    searchQuery.value = query
    await searchStore.search(query)
  }
})

watch(() => route.query.q, async (newQuery) => {
  if (newQuery && typeof newQuery === 'string') {
    searchQuery.value = newQuery
    await searchStore.search(newQuery)
  }
})
</script>

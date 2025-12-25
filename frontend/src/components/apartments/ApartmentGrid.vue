<script setup lang="ts">
import { computed } from 'vue'
import type { Apartment } from '@/types'
import ApartmentCard from './ApartmentCard.vue'

const props = defineProps<{
  apartments: Apartment[]
  loading?: boolean
  emptyMessage?: string
}>()

const emit = defineEmits<{
  (e: 'select', apartment: Apartment): void
}>()

const handleSelect = (apartment: Apartment) => {
  emit('select', apartment)
}
</script>

<template>
  <div>
    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div
        v-for="i in 8"
        :key="i"
        class="bg-white rounded-2xl shadow-md overflow-hidden animate-pulse"
      >
        <div class="h-48 bg-gray-200"></div>
        <div class="p-4 space-y-3">
          <div class="h-5 bg-gray-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          <div class="flex gap-2">
            <div class="h-6 bg-gray-200 rounded w-16"></div>
            <div class="h-6 bg-gray-200 rounded w-16"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="apartments.length === 0"
      class="text-center py-16 px-4"
    >
      <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-1">{{ $t('common.noResultsFound') }}</h3>
      <p class="text-gray-500">{{ emptyMessage || $t('common.tryAdjustingSearch') }}</p>
    </div>

    <!-- Apartments Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ApartmentCard
        v-for="apartment in apartments"
        :key="apartment.id"
        :apartment="apartment"
        @click="handleSelect"
      />
    </div>
  </div>
</template>

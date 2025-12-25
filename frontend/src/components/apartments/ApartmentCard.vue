<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Apartment } from '@/types'

const { t } = useI18n()

const props = defineProps<{
  apartment: Apartment
}>()

const emit = defineEmits<{
  (e: 'click', apartment: Apartment): void
}>()

const imageUrl = computed(() => {
  if (props.apartment.images && props.apartment.images.length > 0) {
    const img = props.apartment.images[0]
    if (img.startsWith('http')) return img
    // If URL already has /static/images/ prefix, just prepend base URL
    if (img.startsWith('/static/images/')) {
      return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${img}`
    }
    // Otherwise, add the prefix
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/static/images/${img}`
  }
  return 'https://via.placeholder.com/400x300?text=No+Image'
})

const formattedPrice = computed(() => {
  return `${props.apartment.rent_per_week.toLocaleString()} EGP/week`
})

const formattedDate = computed(() => {
  if (!props.apartment.start_date) return t('common.availableNow')
  const date = new Date(props.apartment.start_date)
  return `${t('apartments.details.available')} ${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
})

const apartmentTypeLabel = computed(() => {
  const types: Record<string, string> = {
    studio: t('common.studio'),
    '1bhk': '1 BHK',
    '2bhk': '2 BHK',
    '3bhk': '3 BHK',
    '4bhk': '4 BHK',
    villa: t('common.villa'),
    penthouse: t('common.penthouse')
  }
  return types[props.apartment.apartment_type] || props.apartment.apartment_type
})

const handleClick = () => {
  emit('click', props.apartment)
}
</script>

<template>
  <div
    @click="handleClick"
    class="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden cursor-pointer transform hover:-translate-y-1"
  >
    <!-- Image Container -->
    <div class="relative h-48 overflow-hidden">
      <img
        :src="imageUrl"
        :alt="apartment.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />

      <!-- Featured Badge -->
      <div
        v-if="apartment.is_featured"
        class="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-semibold text-white"
        style="background: linear-gradient(90deg, #FF8C42 0%, #E67A3A 100%);"
      >
        {{ $t('apartments.details.featured') }}
      </div>

      <!-- Status Badge -->
      <div
        v-if="apartment.status !== 'published'"
        class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold"
        :class="{
          'bg-yellow-100 text-yellow-800': apartment.status === 'draft',
          'bg-gray-100 text-gray-800': apartment.status === 'archived'
        }"
      >
        {{ apartment.status === 'draft' ? $t('common.draft') : $t('common.archived') }}
      </div>

      <!-- Price Badge -->
      <div
        class="absolute bottom-3 right-3 px-3 py-1.5 rounded-xl text-sm font-bold text-white backdrop-blur-sm"
        style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
      >
        {{ formattedPrice }}
      </div>
    </div>

    <!-- Content -->
    <div class="p-4">
      <!-- Title -->
      <h3 class="text-lg font-semibold text-gray-900 mb-1 line-clamp-1 group-hover:text-secondary-600 transition-colors">
        {{ apartment.title }}
      </h3>

      <!-- Location -->
      <div class="flex items-center text-gray-500 text-sm mb-3">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
        </svg>
        <span class="line-clamp-1">{{ apartment.location }}</span>
      </div>

      <!-- Features Row -->
      <div class="flex items-center gap-3 text-sm text-gray-600 mb-3">
        <!-- Type -->
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          <span>{{ apartmentTypeLabel }}</span>
        </div>

        <!-- Bathroom -->
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/>
          </svg>
          <span>{{ apartment.is_bathroom_solo ? $t('common.private') : $t('common.shared') }}</span>
        </div>
      </div>

      <!-- Keywords/Amenities -->
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="keyword in apartment.keywords?.slice(0, 3)"
          :key="keyword"
          class="px-2 py-0.5 bg-secondary-100 text-secondary-700 text-xs rounded-full"
        >
          {{ keyword }}
        </span>
        <span
          v-if="apartment.keywords && apartment.keywords.length > 3"
          class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full"
        >
          +{{ apartment.keywords.length - 3 }}
        </span>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
        <span class="text-xs text-gray-500">{{ formattedDate }}</span>
        <div class="flex items-center gap-1 text-xs text-gray-500">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
          </svg>
          <span>{{ apartment.view_count || 0 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

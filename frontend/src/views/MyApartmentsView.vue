<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2">{{ $t('myApartments.title') }}</h1>
          <p class="text-gray-400">{{ $t('myApartments.subtitle') }}</p>
        </div>
        <router-link to="/put-an-ad">
          <BaseButton :label="$t('common.newListing')" variant="primary" size="md" />
        </router-link>
      </div>

      <!-- Status Tabs -->
      <div class="flex gap-2 mb-8 overflow-x-auto pb-2">
        <button
          v-for="tab in statusTabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-4 py-2 rounded-xl font-medium transition-all whitespace-nowrap',
            activeTab === tab.value
              ? 'text-white'
              : 'bg-white bg-opacity-10 text-gray-300 hover:bg-opacity-20'
          ]"
          :style="activeTab === tab.value ? { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' } : {}"
        >
          {{ tab.label }}
          <span class="ml-2 px-2 py-0.5 rounded-full text-xs bg-black bg-opacity-30">
            {{ getTabCount(tab.value) }}
          </span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white bg-opacity-5 rounded-2xl overflow-hidden animate-pulse">
          <div class="h-48 bg-gray-700"></div>
          <div class="p-4 space-y-3">
            <div class="h-5 bg-gray-700 rounded w-3/4"></div>
            <div class="h-4 bg-gray-700 rounded w-1/2"></div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredApartments.length === 0" class="text-center py-16">
        <svg class="w-20 h-20 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
        </svg>
        <h3 class="text-xl font-medium text-white mb-2">{{ $t('common.noApartmentsYet') }}</h3>
        <p class="text-gray-400 mb-6">{{ $t('common.startCreatingListing') }}</p>
        <router-link to="/put-an-ad">
          <BaseButton :label="$t('common.createListing')" variant="primary" size="md" />
        </router-link>
      </div>

      <!-- Apartments Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="apartment in filteredApartments"
          :key="apartment.id"
          class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl overflow-hidden border border-white border-opacity-10 hover:border-opacity-20 transition-all"
        >
          <!-- Image -->
          <div class="relative h-48">
            <img
              :src="getImageUrl(apartment.images?.[0])"
              :alt="apartment.title"
              class="w-full h-full object-cover"
            />
            <!-- Status Badge -->
            <div
              class="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-semibold"
              :class="getStatusClass(apartment.status)"
            >
              {{ getStatusLabel(apartment.status) }}
            </div>
            <!-- Featured Badge -->
            <div
              v-if="apartment.is_featured"
              class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold text-white"
              style="background: linear-gradient(90deg, #FF8C42 0%, #E67A3A 100%);"
            >
              {{ $t('apartments.details.featured') }}
            </div>
          </div>

          <!-- Content -->
          <div class="p-4">
            <h3 class="text-lg font-semibold text-white mb-1 line-clamp-1">{{ apartment.title }}</h3>
            <p class="text-gray-400 text-sm mb-3 line-clamp-1">{{ apartment.location }}</p>

            <div class="flex items-center justify-between mb-4">
              <span class="text-xl font-bold text-white">{{ apartment.rent_per_week?.toLocaleString() }} <span class="text-sm font-normal text-gray-400">EGP/week</span></span>
              <div class="flex items-center gap-1 text-gray-400 text-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                {{ apartment.view_count || 0 }} {{ $t('myApartments.views') }}
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2">
              <router-link :to="`/apartments/${apartment.id}`" class="flex-1">
                <button class="w-full px-3 py-2 bg-white bg-opacity-10 text-white rounded-lg text-sm font-medium hover:bg-opacity-20 transition-colors">
                  {{ $t('common.view') }}
                </button>
              </router-link>
              <router-link :to="`/my-apartments/${apartment.id}/edit`" class="flex-1">
                <button class="w-full px-3 py-2 bg-white bg-opacity-10 text-white rounded-lg text-sm font-medium hover:bg-opacity-20 transition-colors">
                  {{ $t('common.edit') }}
                </button>
              </router-link>
              <button
                @click="showActions(apartment)"
                class="px-3 py-2 bg-white bg-opacity-10 text-white rounded-lg hover:bg-opacity-20 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions Dropdown -->
      <div
        v-if="selectedApartment && showActionsDropdown"
        class="fixed inset-0 z-50"
        @click="hideActions"
      >
        <div
          class="absolute bg-gray-800 rounded-xl shadow-xl border border-gray-700 py-2 w-48"
          :style="{ top: dropdownPosition.y + 'px', left: dropdownPosition.x + 'px' }"
          @click.stop
        >
          <button
            v-if="selectedApartment.status === 'draft'"
            @click="handlePublish"
            class="w-full px-4 py-2 text-left text-white hover:bg-gray-700 transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ $t('common.publish') }}
          </button>
          <button
            v-if="selectedApartment.status === 'published'"
            @click="handleArchive"
            class="w-full px-4 py-2 text-left text-white hover:bg-gray-700 transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            {{ $t('common.archive') }}
          </button>
          <button
            @click="handleDuplicate"
            class="w-full px-4 py-2 text-left text-white hover:bg-gray-700 transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            {{ $t('common.duplicate') }}
          </button>
          <button
            @click="handleDelete"
            class="w-full px-4 py-2 text-left text-red-400 hover:bg-gray-700 transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            {{ $t('common.delete') }}
          </button>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div
        v-if="showDeleteModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      >
        <div class="bg-gray-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-gray-700">
          <h3 class="text-xl font-semibold text-white mb-2">{{ $t('common.delete') }} {{ $t('putAnAd.apartmentType') }}</h3>
          <p class="text-gray-400 mb-6">{{ $t('common.deleteConfirmation', { title: selectedApartment?.title }) }}</p>
          <div class="flex gap-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 bg-gray-700 text-white rounded-xl font-medium hover:bg-gray-600 transition-colors"
            >
              {{ $t('common.cancel') }}
            </button>
            <button
              @click="confirmDelete"
              class="flex-1 px-4 py-2 bg-red-600 text-white rounded-xl font-medium hover:bg-red-700 transition-colors"
            >
              {{ $t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApartmentStore } from '@/stores/apartment'
import { useUIStore } from '@/stores/ui'
import type { Apartment } from '@/types'
import BaseButton from '@/components/buttons/BaseButton.vue'

const { t } = useI18n()

const apartmentStore = useApartmentStore()
const uiStore = useUIStore()

const activeTab = ref('all')
const selectedApartment = ref<Apartment | null>(null)
const showActionsDropdown = ref(false)
const showDeleteModal = ref(false)
const dropdownPosition = ref({ x: 0, y: 0 })

const statusTabs = computed(() => [
  { value: 'all', label: t('common.all') },
  { value: 'published', label: t('common.published') },
  { value: 'draft', label: t('common.drafts') },
  { value: 'archived', label: t('common.archived') }
])

const myApartments = computed(() => apartmentStore.myApartments)
const loading = computed(() => apartmentStore.loading)

const filteredApartments = computed(() => {
  if (activeTab.value === 'all') return myApartments.value
  return myApartments.value.filter((a) => a.status === activeTab.value)
})

const getTabCount = (status: string) => {
  if (status === 'all') return myApartments.value.length
  return myApartments.value.filter((a) => a.status === status).length
}

const getImageUrl = (img?: string) => {
  if (!img) return 'https://via.placeholder.com/400x300?text=No+Image'
  if (img.startsWith('http')) return img
  // If URL already has /static/images/ prefix, just prepend base URL
  if (img.startsWith('/static/images/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${img}`
  }
  // Otherwise, add the prefix
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/static/images/${img}`
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'published':
      return 'bg-green-500 bg-opacity-80 text-white'
    case 'draft':
      return 'bg-yellow-500 bg-opacity-80 text-black'
    case 'archived':
      return 'bg-gray-500 bg-opacity-80 text-white'
    default:
      return 'bg-gray-500 bg-opacity-80 text-white'
  }
}

const getStatusLabel = (status: string) => {
  switch (status) {
    case 'published':
      return t('common.published')
    case 'draft':
      return t('common.draft')
    case 'archived':
      return t('common.archived')
    default:
  return status.charAt(0).toUpperCase() + status.slice(1)
  }
}

const showActions = (apartment: Apartment) => {
  selectedApartment.value = apartment
  showActionsDropdown.value = true
  // Position dropdown near the click
  const rect = (event as MouseEvent).target as HTMLElement
  if (rect) {
    const bounds = rect.getBoundingClientRect()
    dropdownPosition.value = {
      x: Math.min(bounds.left, window.innerWidth - 200),
      y: bounds.bottom + 8
    }
  }
}

const hideActions = () => {
  showActionsDropdown.value = false
  selectedApartment.value = null
}

const handlePublish = async () => {
  if (!selectedApartment.value) return
  const success = await apartmentStore.publishApartment(selectedApartment.value.id)
  if (success) {
    uiStore.showSuccess('Apartment published!')
    await apartmentStore.fetchMyApartments()
  } else {
    uiStore.showError('Failed to publish apartment')
  }
  hideActions()
}

const handleArchive = async () => {
  if (!selectedApartment.value) return
  const success = await apartmentStore.archiveApartment(selectedApartment.value.id)
  if (success) {
    uiStore.showSuccess(t('common.apartmentArchived'))
    await apartmentStore.fetchMyApartments()
  } else {
    uiStore.showError(t('common.failedArchiveApartment'))
  }
  hideActions()
}

const handleDuplicate = async () => {
  if (!selectedApartment.value) return
  const result = await apartmentStore.duplicateApartment(selectedApartment.value.id)
  if (result) {
    uiStore.showSuccess(t('common.apartmentDuplicated'))
    await apartmentStore.fetchMyApartments()
  } else {
    uiStore.showError(t('common.failedDuplicateApartment'))
  }
  hideActions()
}

const handleDelete = () => {
  showActionsDropdown.value = false
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!selectedApartment.value) return
  const success = await apartmentStore.deleteApartment(selectedApartment.value.id)
  if (success) {
    uiStore.showSuccess('Apartment deleted!')
  } else {
    uiStore.showError('Failed to delete apartment')
  }
  showDeleteModal.value = false
  selectedApartment.value = null
}

onMounted(() => {
  apartmentStore.fetchMyApartments()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

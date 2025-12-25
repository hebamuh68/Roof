<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <div class="animate-pulse">
        <div class="h-96 bg-gray-700 rounded-2xl mb-8"></div>
        <div class="space-y-4">
          <div class="h-8 bg-gray-700 rounded w-2/3"></div>
          <div class="h-4 bg-gray-700 rounded w-1/3"></div>
          <div class="h-32 bg-gray-700 rounded"></div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="apartment" class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Back Button -->
      <button
        @click="goBack"
        class="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        {{ $t('apartments.backToListings') }}
      </button>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Image Gallery -->
          <div class="relative">
            <div class="aspect-video bg-gray-800 rounded-2xl overflow-hidden">
              <img
                :src="currentImage"
                :alt="apartment.title"
                class="w-full h-full object-cover"
              />

              <!-- Featured Badge -->
              <div
                v-if="apartment.is_featured"
                class="absolute top-4 left-4 px-4 py-2 rounded-full text-sm font-semibold text-white"
                style="background: linear-gradient(90deg, #FF8C42 0%, #E67A3A 100%);"
              >
                {{ $t('apartments.details.featured') }}
              </div>
            </div>

            <!-- Thumbnail Gallery -->
            <div v-if="apartment.images && apartment.images.length > 1" class="flex gap-3 mt-4 overflow-x-auto pb-2">
              <button
                v-for="(image, index) in apartment.images"
                :key="index"
                @click="currentImageIndex = index"
                :class="[
                  'flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all',
                  currentImageIndex === index ? 'border-secondary-500' : 'border-transparent opacity-70 hover:opacity-100'
                ]"
              >
                <img :src="getImageUrl(image)" :alt="`Image ${index + 1}`" class="w-full h-full object-cover" />
              </button>
            </div>
          </div>

          <!-- Title and Price -->
          <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
            <div class="flex flex-wrap items-start justify-between gap-4">
              <div>
                <h1 class="text-2xl sm:text-3xl font-bold text-white mb-2">{{ apartment.title }}</h1>
                <div class="flex items-center text-gray-400">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  {{ apartment.location }}
                </div>
              </div>
              <div class="text-right">
                <div class="text-3xl font-bold text-white">{{ apartment.rent_per_week.toLocaleString() }} <span class="text-lg font-normal text-gray-400">{{ $t('apartments.details.egpWeek') }}</span></div>
                <div class="text-sm text-gray-400 mt-1">{{ formattedDate }}</div>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
            <h2 class="text-xl font-semibold text-white mb-4">{{ $t('apartments.details.aboutPlace') }}</h2>
            <p class="text-gray-300 leading-relaxed whitespace-pre-line">{{ apartment.description }}</p>
          </div>

          <!-- Features -->
          <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
            <h2 class="text-xl font-semibold text-white mb-4">{{ $t('apartments.details.featuresAmenities') }}</h2>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div class="flex items-center gap-3 text-gray-300">
                <div class="w-10 h-10 rounded-lg bg-secondary-500 bg-opacity-20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-400">{{ $t('common.type') }}</div>
                  <div class="font-medium">{{ apartmentTypeLabel }}</div>
                </div>
              </div>

              <div class="flex items-center gap-3 text-gray-300">
                <div class="w-10 h-10 rounded-lg bg-secondary-500 bg-opacity-20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-400">{{ $t('putAnAd.bathroomType') }}</div>
                  <div class="font-medium">{{ apartment.is_bathroom_solo ? $t('common.private') : $t('common.shared') }}</div>
                </div>
              </div>

              <div class="flex items-center gap-3 text-gray-300">
                <div class="w-10 h-10 rounded-lg bg-secondary-500 bg-opacity-20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-400">{{ $t('common.furnishing') }}</div>
                  <div class="font-medium capitalize">{{ apartment.furnishing_type }}</div>
                </div>
              </div>

              <div class="flex items-center gap-3 text-gray-300">
                <div class="w-10 h-10 rounded-lg bg-secondary-500 bg-opacity-20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-400">{{ $t('common.parking') }}</div>
                  <div class="font-medium capitalize">{{ apartment.parking_type || $t('putAnAd.parkingNone') }}</div>
                </div>
              </div>

              <div class="flex items-center gap-3 text-gray-300">
                <div class="w-10 h-10 rounded-lg bg-secondary-500 bg-opacity-20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-400">{{ $t('putAnAd.duration') }}</div>
                  <div class="font-medium">{{ apartment.duration_len ? `${apartment.duration_len} ${$t('common.weeks')}` : $t('common.flexible') }}</div>
                </div>
              </div>

              <div class="flex items-center gap-3 text-gray-300">
                <div class="w-10 h-10 rounded-lg bg-secondary-500 bg-opacity-20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-400">{{ $t('apartments.details.accepts') }}</div>
                  <div class="font-medium capitalize">{{ apartment.place_accept || $t('common.anyone') }}</div>
                </div>
              </div>
            </div>

            <!-- Keywords -->
            <div v-if="apartment.keywords && apartment.keywords.length > 0" class="mt-6 pt-6 border-t border-white border-opacity-10">
              <h3 class="text-sm font-medium text-gray-400 mb-3">{{ $t('common.amenities') }}</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="keyword in apartment.keywords"
                  :key="keyword"
                  class="px-3 py-1.5 bg-secondary-500 bg-opacity-20 text-secondary-300 rounded-full text-sm"
                >
                  {{ keyword }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Contact Card -->
          <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10 sticky top-24">
            <h3 class="text-lg font-semibold text-white mb-4">{{ $t('apartments.details.contactOwner') }}</h3>

            <div v-if="isAuthenticated">
              <textarea
                v-model="messageContent"
                rows="4"
                :placeholder="$t('apartments.details.writeMessage')"
                class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 resize-none mb-4"
              ></textarea>

              <BaseButton
                @click="sendInquiry"
                :loading="sendingMessage"
                :label="$t('messages.sendMessage')"
                variant="primary"
                size="md"
                block
              />
            </div>

            <div v-else class="text-center">
              <p class="text-gray-400 mb-4">{{ $t('apartments.details.contactOwner') }}</p>
              <router-link to="/login">
                <BaseButton
                  :label="$t('nav.login')"
                  variant="primary"
                  size="md"
                  block
                />
              </router-link>
            </div>

            <!-- Stats -->
            <div class="flex items-center justify-between mt-6 pt-6 border-t border-white border-opacity-10 text-gray-400 text-sm">
              <div class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <span>{{ apartment.view_count || 0 }} {{ $t('myApartments.views') }}</span>
              </div>
              <div>Listed {{ listedDate }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12 text-center">
      <svg class="w-24 h-24 mx-auto text-gray-600 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
      </svg>
      <h2 class="text-2xl font-bold text-white mb-2">{{ $t('common.apartmentNotFoundTitle') }}</h2>
      <p class="text-gray-400 mb-6">{{ $t('common.apartmentRemoved') }}</p>
      <router-link to="/apartments">
        <BaseButton label="Browse Apartments" variant="primary" size="md" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useApartmentStore } from '@/stores/apartment'
import { useAuthStore } from '@/stores/auth'
import { useMessageStore } from '@/stores/message'
import { useUIStore } from '@/stores/ui'
import BaseButton from '@/components/buttons/BaseButton.vue'

const { t } = useI18n()

const route = useRoute()
const router = useRouter()
const apartmentStore = useApartmentStore()
const authStore = useAuthStore()
const messageStore = useMessageStore()
const uiStore = useUIStore()

const currentImageIndex = ref(0)
const messageContent = ref('')
const sendingMessage = ref(false)

const apartment = computed(() => apartmentStore.currentApartment)
const loading = computed(() => apartmentStore.loading)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const currentImage = computed(() => {
  if (!apartment.value?.images?.length) return 'https://via.placeholder.com/800x600?text=No+Image'
  return getImageUrl(apartment.value.images[currentImageIndex.value])
})

const getImageUrl = (img: string) => {
  if (img.startsWith('http')) return img
  // If URL already has /static/images/ prefix, just prepend base URL
  if (img.startsWith('/static/images/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${img}`
  }
  // Otherwise, add the prefix
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/static/images/${img}`
}

const apartmentTypeLabel = computed(() => {
  const types: Record<string, string> = {
    studio: 'Studio',
    '1bhk': '1 BHK',
    '2bhk': '2 BHK',
    '3bhk': '3 BHK',
    '4bhk': '4 BHK',
    villa: 'Villa',
    penthouse: 'Penthouse'
  }
  return types[apartment.value?.apartment_type || ''] || apartment.value?.apartment_type
})

const formattedDate = computed(() => {
  if (!apartment.value?.start_date) return 'Available now'
  const date = new Date(apartment.value.start_date)
  return `Available from ${date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}`
})

const listedDate = computed(() => {
  if (!apartment.value?.created_at) return ''
  const date = new Date(apartment.value.created_at)
  const now = new Date()
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
})

const goBack = () => {
  router.back()
}

const sendInquiry = async () => {
  if (!messageContent.value.trim() || !apartment.value) return

  sendingMessage.value = true
  try {
    const result = await messageStore.sendMessage({
      receiver_id: apartment.value.renter_id,
      content: messageContent.value,
      apartment_id: apartment.value.id
    })

    if (result) {
      uiStore.showSuccess('Message sent successfully!')
      messageContent.value = ''
    } else {
      uiStore.showError(messageStore.error || 'Failed to send message')
    }
  } catch (error) {
    uiStore.showError('Failed to send message')
  } finally {
    sendingMessage.value = false
  }
}

onMounted(async () => {
  const id = Number(route.params.id)
  if (id) {
    await apartmentStore.fetchApartment(id)
  }
})
</script>

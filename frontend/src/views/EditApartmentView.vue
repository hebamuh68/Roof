<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <div class="animate-pulse space-y-8">
        <div class="h-8 bg-gray-700 rounded w-1/3"></div>
        <div class="bg-gray-700 rounded-2xl h-96"></div>
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="apartment" class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="flex items-center gap-4 mb-8">
        <button @click="goBack" class="p-2 hover:bg-white hover:bg-opacity-10 rounded-lg transition-colors">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <div>
          <h1 class="text-3xl sm:text-4xl font-bold text-white mb-1">Edit Apartment</h1>
          <p class="text-gray-400">Update your listing details</p>
        </div>
      </div>

      <!-- Form Card -->
      <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 sm:p-8 border border-white border-opacity-10">
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <!-- Basic Info Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">Basic Information</h2>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Title *</label>
                <input
                  v-model="form.title"
                  type="text"
                  required
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Description *</label>
                <textarea
                  v-model="form.description"
                  rows="4"
                  required
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 resize-none transition-all"
                ></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Location *</label>
                <input
                  v-model="form.location"
                  type="text"
                  required
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Property Details -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">Property Details</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Apartment Type</label>
                <select
                  v-model="form.apartment_type"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="studio" class="bg-gray-800">Studio</option>
                  <option value="1bhk" class="bg-gray-800">1 BHK</option>
                  <option value="2bhk" class="bg-gray-800">2 BHK</option>
                  <option value="3bhk" class="bg-gray-800">3 BHK</option>
                  <option value="4bhk" class="bg-gray-800">4 BHK</option>
                  <option value="villa" class="bg-gray-800">Villa</option>
                  <option value="penthouse" class="bg-gray-800">Penthouse</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Rent per Week (EGP)</label>
                <input
                  v-model.number="form.rent_per_week"
                  type="number"
                  min="1"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Available From</label>
                <input
                  v-model="form.start_date"
                  type="date"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Duration (weeks)</label>
                <input
                  v-model.number="form.duration_len"
                  type="number"
                  min="1"
                  placeholder="Flexible"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Furnishing</label>
                <select
                  v-model="form.furnishing_type"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="furnished" class="bg-gray-800">Furnished</option>
                  <option value="semi-furnished" class="bg-gray-800">Semi-Furnished</option>
                  <option value="unfurnished" class="bg-gray-800">Unfurnished</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Parking</label>
                <select
                  v-model="form.parking_type"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="none" class="bg-gray-800">None</option>
                  <option value="street" class="bg-gray-800">Street</option>
                  <option value="garage" class="bg-gray-800">Garage</option>
                  <option value="covered" class="bg-gray-800">Covered</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Submit -->
          <div class="flex gap-4 pt-4">
            <button
              type="button"
              @click="goBack"
              class="flex-1 px-8 py-4 bg-gray-700 text-white rounded-full font-semibold hover:bg-gray-600 transition-all"
            >
              Cancel
            </button>
            <BaseButton
              button-type="submit"
              :loading="saving"
              label="Save Changes"
              variant="primary"
              size="md"
              class="flex-1"
            />
          </div>

          <p v-if="error" class="text-red-400 text-center">{{ error }}</p>
        </form>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12 text-center">
      <h2 class="text-2xl font-bold text-white mb-2">Apartment Not Found</h2>
      <p class="text-gray-400 mb-6">The apartment you're trying to edit doesn't exist.</p>
      <router-link to="/my-apartments">
        <BaseButton label="Back to My Apartments" variant="primary" size="md" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApartmentStore } from '@/stores/apartment'
import { useUIStore } from '@/stores/ui'
import BaseButton from '@/components/buttons/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const apartmentStore = useApartmentStore()
const uiStore = useUIStore()

const form = reactive({
  title: '',
  description: '',
  location: '',
  apartment_type: '',
  rent_per_week: 0,
  start_date: '',
  duration_len: null as number | null,
  furnishing_type: '',
  parking_type: '',
  is_bathroom_solo: true,
  place_accept: 'any',
  keywords: [] as string[]
})

const saving = ref(false)
const error = ref('')

const apartment = ref(apartmentStore.currentApartment)
const loading = ref(true)

const goBack = () => {
  router.push({ name: 'myApartments' })
}

const handleSubmit = async () => {
  saving.value = true
  error.value = ''

  try {
    const success = await apartmentStore.updateApartment(Number(route.params.id), form)
    if (success) {
      uiStore.showSuccess('Apartment updated successfully!')
      router.push({ name: 'myApartments' })
    } else {
      error.value = apartmentStore.error || 'Failed to update apartment'
    }
  } catch (err: any) {
    error.value = err.message || 'Something went wrong'
  } finally {
    saving.value = false
  }
}

// Populate form when apartment is loaded
watch(() => apartmentStore.currentApartment, (apt) => {
  if (apt) {
    apartment.value = apt
    form.title = apt.title
    form.description = apt.description
    form.location = apt.location
    form.apartment_type = apt.apartment_type
    form.rent_per_week = apt.rent_per_week
    form.start_date = apt.start_date
    form.duration_len = apt.duration_len
    form.furnishing_type = apt.furnishing_type
    form.parking_type = apt.parking_type
    form.is_bathroom_solo = apt.is_bathroom_solo
    form.place_accept = apt.place_accept
    form.keywords = [...(apt.keywords || [])]
  }
}, { immediate: true })

onMounted(async () => {
  const id = Number(route.params.id)
  if (id) {
    await apartmentStore.fetchApartment(id)
  }
  loading.value = false
})
</script>

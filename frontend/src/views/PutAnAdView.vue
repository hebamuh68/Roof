<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute top-20 -left-20 w-72 h-72 rounded-full blur-3xl opacity-10" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute bottom-20 -right-20 w-72 h-72 rounded-full blur-3xl opacity-10" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <div class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2">{{ $t('putAnAd.title') }}</h1>
        <p class="text-gray-400">{{ $t('putAnAd.subtitle') }}</p>
      </div>

      <!-- Form Card -->
      <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 sm:p-8 border border-white border-opacity-10">
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <!-- Basic Info Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">1</span>
              {{ $t('putAnAd.basicInfo') }}
            </h2>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.titleLabel') }} *</label>
                <input
                  v-model="form.title"
                  type="text"
                  required
                  :placeholder="$t('putAnAd.titlePlaceholder')"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.description') }} *</label>
                <textarea
                  v-model="form.description"
                  rows="4"
                  required
                  :placeholder="$t('putAnAd.descriptionPlaceholder')"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 resize-none transition-all"
                ></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.location') }} *</label>
                <input
                  v-model="form.location"
                  type="text"
                  required
                  :placeholder="$t('putAnAd.location')"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Property Details Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">2</span>
              {{ $t('putAnAd.propertyDetails') }}
            </h2>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.apartmentType') }} *</label>
                <select
                  v-model="form.apartment_type"
                  required
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="" disabled class="bg-gray-800">{{ $t('putAnAd.selectType') }}</option>
                  <option value="studio" class="bg-gray-800">{{ $t('common.studio') }}</option>
                  <option value="1bhk" class="bg-gray-800">1 BHK</option>
                  <option value="2bhk" class="bg-gray-800">2 BHK</option>
                  <option value="3bhk" class="bg-gray-800">3 BHK</option>
                  <option value="4bhk" class="bg-gray-800">4 BHK</option>
                  <option value="villa" class="bg-gray-800">{{ $t('common.villa') }}</option>
                  <option value="penthouse" class="bg-gray-800">{{ $t('common.penthouse') }}</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.rentPerWeek') }} *</label>
                <input
                  v-model.number="form.rent_per_week"
                  type="number"
                  min="1"
                  required
                  placeholder="e.g., 500"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.availableFrom') }} *</label>
                <input
                  v-model="form.start_date"
                  type="date"
                  required
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.duration') }}</label>
                <input
                  v-model.number="form.duration_len"
                  type="number"
                  min="1"
                  :placeholder="$t('putAnAd.durationPlaceholder')"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.furnishingType') }} *</label>
                <select
                  v-model="form.furnishing_type"
                  required
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="" disabled class="bg-gray-800">{{ $t('putAnAd.selectFurnishing') }}</option>
                  <option value="furnished" class="bg-gray-800">{{ $t('putAnAd.furnished') }}</option>
                  <option value="semi-furnished" class="bg-gray-800">{{ $t('putAnAd.semiFurnished') }}</option>
                  <option value="unfurnished" class="bg-gray-800">{{ $t('putAnAd.unfurnished') }}</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.parking') }}</label>
                <select
                  v-model="form.parking_type"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="none" class="bg-gray-800">{{ $t('putAnAd.parkingNone') }}</option>
                  <option value="street" class="bg-gray-800">{{ $t('putAnAd.parkingStreet') }}</option>
                  <option value="garage" class="bg-gray-800">{{ $t('putAnAd.parkingGarage') }}</option>
                  <option value="covered" class="bg-gray-800">{{ $t('putAnAd.parkingCovered') }}</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.bathroomType') }}</label>
                <div class="flex gap-4 mt-1">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" :value="true" v-model="form.is_bathroom_solo" class="w-4 h-4 text-secondary-500" />
                    <span class="text-gray-300">{{ $t('putAnAd.bathroomPrivate') }}</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" :value="false" v-model="form.is_bathroom_solo" class="w-4 h-4 text-secondary-500" />
                    <span class="text-gray-300">{{ $t('putAnAd.bathroomShared') }}</span>
                  </label>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.genderPreference') }}</label>
                <select
                  v-model="form.place_accept"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                >
                  <option value="any" class="bg-gray-800">{{ $t('common.anyone') }}</option>
                  <option value="male" class="bg-gray-800">{{ $t('putAnAd.genderMale') }}</option>
                  <option value="female" class="bg-gray-800">{{ $t('putAnAd.genderFemale') }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Amenities Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">3</span>
              {{ $t('common.amenities') }}
            </h2>

            <div class="flex flex-wrap gap-2">
              <button
                v-for="amenity in availableAmenities"
                :key="amenity"
                type="button"
                @click="toggleAmenity(amenity)"
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium transition-all',
                  form.keywords.includes(amenity)
                    ? 'text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                ]"
                :style="form.keywords.includes(amenity) ? { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' } : {}"
              >
                {{ amenity }}
              </button>
            </div>
          </div>

          <!-- Images Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">4</span>
              {{ $t('putAnAd.images') }}
            </h2>

            <ImageUpload
              v-model="images"
              :min-files="4"
              :max-files="10"
            />
          </div>

          <!-- Submit Section -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <BaseButton
              type="button"
              @click="saveDraft"
              :loading="savingDraft"
              :label="$t('putAnAd.saveAsDraft')"
              variant="outline"
              size="md"
              class="flex-1 !border-gray-500 !text-gray-300 hover:!bg-gray-700"
            />
            <BaseButton
              button-type="submit"
              :loading="submitting"
              :disabled="!isFormValid"
              :label="$t('putAnAd.submit')"
              variant="primary"
              size="md"
              class="flex-1"
            />
          </div>

          <!-- Error Message -->
          <p v-if="error" class="text-red-400 text-center">{{ error }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'

import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useApartmentStore } from '@/stores/apartment'
import { useUIStore } from '@/stores/ui'
import type { ApartmentCreate } from '@/types'
import BaseButton from '@/components/buttons/BaseButton.vue'
import ImageUpload from '@/components/apartments/ImageUpload.vue'

const { t } = useI18n()

const router = useRouter()
const apartmentStore = useApartmentStore()
const uiStore = useUIStore()

const form = reactive<ApartmentCreate>({
  title: '',
  description: '',
  location: '',
  apartment_type: '',
  rent_per_week: 0,
  start_date: '',
  duration_len: null,
  place_accept: 'any',
  furnishing_type: '',
  is_bathroom_solo: true,
  parking_type: 'none',
  keywords: [],
  is_active: true,
  status: 'published'
})

const images = ref<File[]>([])
const submitting = ref(false)
const savingDraft = ref(false)
const error = ref('')

const availableAmenities = [
  t('common.wifi'),
  'AC',
  t('common.heating'),
  t('common.washingMachine'),
  t('common.dryer'),
  t('common.kitchen'),
  'TV',
  t('common.balcony'),
  t('common.garden'),
  t('common.pool'),
  t('common.gym'),
  t('common.security'),
  t('common.elevator'),
  t('common.petFriendly'),
  t('common.smokingAllowed'),
  t('common.utilitiesIncluded')
]

const isFormValid = computed(() => {
  return (
    form.title.trim() &&
    form.description.trim() &&
    form.location.trim() &&
    form.apartment_type &&
    form.rent_per_week > 0 &&
    form.start_date &&
    form.furnishing_type &&
    images.value.length >= 4
  )
})

const toggleAmenity = (amenity: string) => {
  const index = form.keywords.indexOf(amenity)
  if (index > -1) {
    form.keywords.splice(index, 1)
  } else {
    form.keywords.push(amenity)
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value) return

  submitting.value = true
  error.value = ''

  try {
    const result = await apartmentStore.createApartment(form, images.value)
    if (result) {
      uiStore.showSuccess(t('common.apartmentPublished'))
      router.push({ name: 'myApartments' })
    } else {
      error.value = apartmentStore.error || t('common.failedCreateApartment')
    }
  } catch (err: any) {
    error.value = err.message || t('common.somethingWentWrong')
  } finally {
    submitting.value = false
  }
}

const saveDraft = async () => {
  savingDraft.value = true
  error.value = ''

  try {
    const draftForm = { ...form, status: 'draft' as const }
    const result = await apartmentStore.createApartment(draftForm, images.value)
    if (result) {
      uiStore.showSuccess(t('common.draftSaved'))
      router.push({ name: 'myApartments' })
    } else {
      error.value = apartmentStore.error || t('common.failedSaveDraft')
    }
  } catch (err: any) {
    error.value = err.message || t('common.somethingWentWrong')
  } finally {
    savingDraft.value = false
  }
}
</script>

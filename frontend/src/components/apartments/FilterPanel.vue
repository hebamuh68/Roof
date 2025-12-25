<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { ApartmentFilters } from '@/types'
import BaseButton from '@/components/buttons/BaseButton.vue'

const { t } = useI18n()

const props = defineProps<{
  modelValue: ApartmentFilters
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: ApartmentFilters): void
  (e: 'apply'): void
  (e: 'clear'): void
}>()

const isOpen = ref(false)

const filters = ref<ApartmentFilters>({ ...props.modelValue })

watch(() => props.modelValue, (newVal) => {
  filters.value = { ...newVal }
}, { deep: true })

const apartmentTypes = computed(() => [
  { value: '', label: t('common.anyType') },
  { value: 'studio', label: t('common.studio') },
  { value: '1bhk', label: '1 BHK' },
  { value: '2bhk', label: '2 BHK' },
  { value: '3bhk', label: '3 BHK' },
  { value: '4bhk', label: '4 BHK' },
  { value: 'villa', label: t('common.villa') },
  { value: 'penthouse', label: t('common.penthouse') }
])

const furnishingTypes = computed(() => [
  { value: '', label: t('common.any') },
  { value: 'furnished', label: t('putAnAd.furnished') },
  { value: 'semi-furnished', label: t('putAnAd.semiFurnished') },
  { value: 'unfurnished', label: t('putAnAd.unfurnished') }
])

const parkingTypes = computed(() => [
  { value: '', label: t('common.any') },
  { value: 'none', label: t('putAnAd.parkingNone') },
  { value: 'street', label: t('putAnAd.parkingStreet') },
  { value: 'garage', label: t('putAnAd.parkingGarage') },
  { value: 'covered', label: t('putAnAd.parkingCovered') }
])

const genderPreferences = computed(() => [
  { value: '', label: t('common.any') },
  { value: 'any', label: t('putAnAd.genderNoPreference') },
  { value: 'male', label: t('putAnAd.genderMale') },
  { value: 'female', label: t('putAnAd.genderFemale') }
])

const applyFilters = () => {
  emit('update:modelValue', filters.value)
  emit('apply')
  isOpen.value = false
}

const clearFilters = () => {
  filters.value = {}
  emit('update:modelValue', {})
  emit('clear')
}

const togglePanel = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <div class="relative">
    <!-- Filter Toggle Button -->
    <button
      @click="togglePanel"
      class="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-200 rounded-xl shadow-sm hover:bg-gray-50 transition-colors"
    >
      <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
      </svg>
      <span class="font-medium text-gray-700">{{ $t('common.filters') }}</span>
      <span
        v-if="Object.keys(modelValue).filter(k => modelValue[k as keyof ApartmentFilters]).length > 0"
        class="ml-1 px-2 py-0.5 text-xs font-semibold text-white rounded-full"
        style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
      >
        {{ Object.keys(modelValue).filter(k => modelValue[k as keyof ApartmentFilters]).length }}
      </span>
    </button>

    <!-- Filter Panel -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div
        v-if="isOpen"
        class="absolute top-full left-0 mt-2 w-80 sm:w-96 bg-white rounded-2xl shadow-xl border border-gray-100 z-50 overflow-hidden"
      >
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">{{ $t('common.filters') }}</h3>
            <button @click="isOpen = false" class="p-1 hover:bg-gray-100 rounded-lg transition-colors">
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-4 space-y-4 max-h-96 overflow-y-auto">
          <!-- Location -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('apartments.details.location') }}</label>
            <input
              v-model="filters.location"
              type="text"
              :placeholder="$t('common.enterLocation')"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
            />
          </div>

          <!-- Apartment Type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('putAnAd.apartmentType') }}</label>
            <select
              v-model="filters.apartment_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
            >
              <option v-for="type in apartmentTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>

          <!-- Price Range -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('common.priceRange') }}</label>
            <div class="flex items-center gap-2">
              <input
                v-model.number="filters.min_price"
                type="number"
                :placeholder="$t('common.min')"
                min="0"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
              />
              <span class="text-gray-400">-</span>
              <input
                v-model.number="filters.max_price"
                type="number"
                :placeholder="$t('common.max')"
                min="0"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
              />
            </div>
          </div>

          <!-- Furnishing -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('common.furnishing') }}</label>
            <select
              v-model="filters.furnishing_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
            >
              <option v-for="type in furnishingTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>

          <!-- Bathroom -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('putAnAd.bathroomType') }}</label>
            <div class="flex gap-3">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  :value="undefined"
                  v-model="filters.is_bathroom_solo"
                  class="w-4 h-4 text-secondary-500"
                />
                <span class="text-sm text-gray-600">{{ $t('putAnAd.bathroomAny') }}</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  :value="true"
                  v-model="filters.is_bathroom_solo"
                  class="w-4 h-4 text-secondary-500"
                />
                <span class="text-sm text-gray-600">{{ $t('common.private') }}</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  :value="false"
                  v-model="filters.is_bathroom_solo"
                  class="w-4 h-4 text-secondary-500"
                />
                <span class="text-sm text-gray-600">{{ $t('common.shared') }}</span>
              </label>
            </div>
          </div>

          <!-- Parking -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('common.parking') }}</label>
            <select
              v-model="filters.parking_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
            >
              <option v-for="type in parkingTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>

          <!-- Gender Preference -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('common.genderPreference') }}</label>
            <select
              v-model="filters.place_accept"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 transition-colors"
            >
              <option v-for="pref in genderPreferences" :key="pref.value" :value="pref.value">
                {{ pref.label }}
              </option>
            </select>
          </div>
        </div>

        <!-- Actions -->
        <div class="p-4 border-t border-gray-100 flex items-center gap-3">
          <button
            @click="clearFilters"
            class="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 rounded-xl font-medium hover:bg-gray-50 transition-colors"
          >
            {{ $t('common.clearAll') }}
          </button>
          <BaseButton
            @click="applyFilters"
            :loading="loading"
            :label="$t('apartments.filters.apply')"
            variant="primary"
            size="sm"
            class="flex-1"
          />
        </div>
      </div>
    </Transition>

    <!-- Backdrop -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-40"
      @click="isOpen = false"
    ></div>
  </div>
</template>

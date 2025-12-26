<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute top-40 w-72 h-72 rounded-full blur-3xl opacity-10 orb-start" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute bottom-40 w-72 h-72 rounded-full blur-3xl opacity-10 orb-end" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <div class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-heading-1 text-white mb-6">{{ $t('about.heroTitle') }}</h1>
        <p class="text-body-lg text-gray-400 max-w-3xl mx-auto">
          {{ $t('about.heroSubtitle') }}
        </p>
      </div>

      <!-- Mission Section -->
      <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-8 border border-white border-opacity-10 mb-8">
        <div class="flex items-start gap-4 mb-6">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-heading-2 text-white mb-2">{{ $t('about.mission') }}</h2>
            <p class="text-body text-gray-300 leading-relaxed">
              {{ $t('about.missionText') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10 text-center">
          <div class="w-16 h-16 mx-auto rounded-2xl bg-secondary-500 bg-opacity-20 flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <h3 class="text-heading-3 text-white mb-2">{{ $t('about.easySearch') }}</h3>
          <p class="text-body-sm text-gray-400">{{ $t('about.easySearchText') }}</p>
        </div>

        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10 text-center">
          <div class="w-16 h-16 mx-auto rounded-2xl bg-blue-500 bg-opacity-20 flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <h3 class="text-heading-3 text-white mb-2">{{ $t('about.verifiedListings') }}</h3>
          <p class="text-body-sm text-gray-400">{{ $t('about.verifiedListingsText') }}</p>
        </div>

        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10 text-center">
          <div class="w-16 h-16 mx-auto rounded-2xl bg-purple-500 bg-opacity-20 flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
          </div>
          <h3 class="text-heading-3 text-white mb-2">{{ $t('about.directMessaging') }}</h3>
          <p class="text-body-sm text-gray-400">{{ $t('about.directMessagingText') }}</p>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-8 border border-white border-opacity-10 mb-8">
        <h2 class="text-heading-2 text-white text-center mb-8">{{ $t('about.byNumbers') }}</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <div class="text-3xl sm:text-4xl font-bold text-white mb-2">1000+</div>
            <div class="text-gray-400">{{ $t('about.activeListings') }}</div>
          </div>
          <div>
            <div class="text-3xl sm:text-4xl font-bold text-white mb-2">5000+</div>
            <div class="text-gray-400">{{ $t('about.happyUsers') }}</div>
          </div>
          <div>
            <div class="text-3xl sm:text-4xl font-bold text-white mb-2">50+</div>
            <div class="text-gray-400">{{ $t('about.citiesCovered') }}</div>
          </div>
          <div>
            <div class="text-3xl sm:text-4xl font-bold text-white mb-2">98%</div>
            <div class="text-gray-400">{{ $t('about.satisfactionRate') }}</div>
          </div>
        </div>
      </div>

      <!-- Team Section -->
      <div class="text-center">
        <h2 class="text-heading-2 text-white mb-4">{{ $t('about.builtWithCare') }}</h2>
        <p class="text-body text-gray-400 max-w-2xl mx-auto mb-8">
          {{ $t('about.builtWithCareText') }}
        </p>
        <router-link to="/contact">
          <BaseButton :label="$t('about.getInTouch')" variant="primary" size="md" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import BaseButton from '@/components/buttons/BaseButton.vue'

const { t } = useI18n()
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

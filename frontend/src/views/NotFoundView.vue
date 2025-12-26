<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute top-20 w-72 h-72 rounded-full blur-3xl opacity-10 orb-start" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute bottom-20 w-72 h-72 rounded-full blur-3xl opacity-10 orb-end" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <div class="relative text-center px-4">
      <div class="text-9xl font-bold text-white mb-4 opacity-20">404</div>
      <h1 class="text-heading-1 text-white mb-4">{{ $t('common.pageNotFound') }}</h1>
      <p class="text-body text-gray-400 mb-8 max-w-md mx-auto">
        {{ $t('common.pageMoved') }}
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <router-link to="/">
          <BaseButton :label="$t('common.goHome')" variant="primary" size="md" />
        </router-link>
        <router-link to="/apartments">
          <button class="px-8 py-4 bg-white bg-opacity-10 border border-white border-opacity-20 text-white rounded-full font-semibold hover:bg-opacity-20 transition-all">
            {{ $t('common.browseApartments') }}
          </button>
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

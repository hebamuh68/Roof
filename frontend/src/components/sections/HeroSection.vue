<template>
  <div class="relative w-screen h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background image with overlay -->
    <img :src="heroBkg" alt="Hero Section" class="w-full h-full object-cover absolute top-0 left-0 z-10 opacity-30" />

    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10 z-20">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute -top-20 w-72 h-72 rounded-full blur-3xl opacity-20 z-20 hero-orb-start" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute -bottom-20 w-72 h-72 rounded-full blur-3xl opacity-20 z-20 hero-orb-end" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <!-- Content -->
    <div :class="[
      'absolute top-1/2 -translate-y-1/2 z-30 text-white max-w-2xl px-6 sm:px-8 lg:px-0',
      isRTL ? 'right-8 sm:right-16 lg:right-32' : 'left-8 sm:left-16 lg:left-32'
    ]">
      <h1 class="text-display mb-6 leading-tight drop-shadow-lg">
        {{ $t('hero.welcome') }} <br>
        <span class="text-green-400">{{ $t('hero.roof') }}</span>
      </h1>
      <p class="text-body-lg mb-8 text-gray-200 drop-shadow max-w-lg">
        {{ $t('hero.subtitle') }}
      </p>
      <router-link to="/signup">
        <BaseButton :label="$t('hero.getStarted')" variant="primary" size="lg" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLanguageStore } from '@/stores/language'
import heroBkg from '@/assets/images/heroBkg.png'
import BaseButton from '../buttons/BaseButton.vue'

const { t } = useI18n()
const languageStore = useLanguageStore()
const isRTL = computed(() => languageStore.getCurrentLanguage().dir === 'rtl')
</script>

<style scoped>
.hero-orb-start {
  left: -5rem;
}

.hero-orb-end {
  right: -5rem;
}

[dir="rtl"] .hero-orb-start {
  left: auto;
  right: -5rem;
}

[dir="rtl"] .hero-orb-end {
  right: auto;
  left: -5rem;
}
</style>

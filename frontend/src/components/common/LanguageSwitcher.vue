<template>
  <div class="relative">
    <button
      @click="toggleDropdown"
      :class="[
        'flex items-center gap-2 px-3 py-2 rounded-lg transition-colors text-sm font-medium',
        isHomePage
          ? 'text-white/70 hover:text-white bg-white/10'
          : 'text-gray-500 hover:text-gray-700 bg-gray-100'
      ]"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
      </svg>
      <span>{{ currentLanguage.nativeName }}</span>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </button>

    <!-- Dropdown -->
    <Transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div
        v-if="isOpen"
        :class="[
          'absolute mt-2 w-48 rounded-xl shadow-lg border py-2 z-50',
          isRTL ? 'left-0' : 'right-0',
          isHomePage
            ? 'bg-gray-900 border-gray-700'
            : 'bg-white border-gray-100'
        ]"
      >
        <button
          v-for="lang in supportedLanguages"
          :key="lang.code"
          @click="selectLanguage(lang.code)"
          :class="[
            'w-full text-left px-4 py-2 text-sm transition-colors flex items-center justify-between',
            isHomePage
              ? currentLanguage.code === lang.code
                ? 'bg-white/20 text-white'
                : 'text-gray-300 hover:bg-white/10 hover:text-white'
              : currentLanguage.code === lang.code
                ? 'bg-green-50 text-green'
                : 'text-gray-700 hover:bg-gray-50'
          ]"
        >
          <span>{{ lang.nativeName }}</span>
          <span v-if="currentLanguage.code === lang.code" class="text-green-500">✓</span>
        </button>
      </div>
    </Transition>

    <!-- Backdrop -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-40"
      @click="closeDropdown"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLanguageStore } from '@/stores/language'

const route = useRoute()
const languageStore = useLanguageStore()

const isOpen = ref(false)
const isHomePage = computed(() => route.name === 'home')
const isRTL = computed(() => languageStore.getCurrentLanguage().dir === 'rtl')

const currentLanguage = computed(() => languageStore.getCurrentLanguage())
const supportedLanguages = computed(() => languageStore.supportedLanguages)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const selectLanguage = (langCode: string) => {
  languageStore.setLanguage(langCode)
  closeDropdown()
}

// Close dropdown on outside click
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>


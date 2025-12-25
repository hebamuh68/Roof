<script setup>
import { onMounted, watch } from 'vue'
import { useLanguageStore } from './stores/language'
import Navbar from './components/common/Navbar.vue'
import ToastContainer from './components/common/ToastContainer.vue'

const languageStore = useLanguageStore()

// Ensure direction is set on mount and when language changes
onMounted(() => {
  const currentLang = languageStore.getCurrentLanguage()
  document.documentElement.dir = currentLang.dir
  document.documentElement.lang = currentLang.code
})

watch(() => languageStore.currentLanguage, (newLang) => {
  const lang = languageStore.getCurrentLanguage()
  document.documentElement.dir = lang.dir
  document.documentElement.lang = lang.code
})
</script>

<template>
  <Navbar />
  <router-view />
  <ToastContainer />
</template>

<style>
@import '@/assets/base.css';

/* Remove default margins and padding for full-screen layout */
body {
  margin: 0;
  padding: 0;
  background-color: #f0f0f0;
}

#app {
  margin: 0;
  padding: 0;
  min-height: 100vh;
}
</style>

import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import i18n from '@/i18n'

export const useLanguageStore = defineStore('language', () => {
  // Supported languages
  const supportedLanguages = [
    { code: 'en', name: 'English', nativeName: 'English', dir: 'ltr' },
    { code: 'ar', name: 'Arabic', nativeName: 'العربية', dir: 'rtl' },
    { code: 'fr', name: 'French', nativeName: 'Français', dir: 'ltr' },
    { code: 'it', name: 'Italian', nativeName: 'Italiano', dir: 'ltr' },
    { code: 'ru', name: 'Russian', nativeName: 'Русский', dir: 'ltr' }
  ]

  // Get current language from localStorage or default to 'en'
  const currentLanguage = ref<string>(localStorage.getItem('locale') || 'en')

  // Set language
  const setLanguage = (langCode: string) => {
    const language = supportedLanguages.find(lang => lang.code === langCode)
    if (language) {
      currentLanguage.value = langCode
      i18n.global.locale.value = langCode
      localStorage.setItem('locale', langCode)
      
      // Update document direction for RTL languages
      document.documentElement.dir = language.dir
      document.documentElement.lang = langCode
    }
  }

  // Get current language info
  const getCurrentLanguage = () => {
    return supportedLanguages.find(lang => lang.code === currentLanguage.value) || supportedLanguages[0]
  }

  // Initialize language on store creation
  const initializeLanguage = () => {
    const savedLang = localStorage.getItem('locale') || 'en'
    setLanguage(savedLang)
  }

  // Watch for language changes and update document
  watch(currentLanguage, (newLang) => {
    const language = supportedLanguages.find(lang => lang.code === newLang)
    if (language) {
      document.documentElement.dir = language.dir
      document.documentElement.lang = newLang
    }
  })

  return {
    currentLanguage,
    supportedLanguages,
    setLanguage,
    getCurrentLanguage,
    initializeLanguage
  }
})


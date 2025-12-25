import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import i18n from './i18n'

import './assets/base.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)

// Initialize auth state from localStorage
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.initializeAuth()

// Initialize language state
import { useLanguageStore } from './stores/language'
const languageStore = useLanguageStore()
languageStore.initializeLanguage()

app.mount('#app')

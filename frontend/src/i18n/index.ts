import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import ar from './locales/ar.json'
import fr from './locales/fr.json'
import it from './locales/it.json'
import ru from './locales/ru.json'

// Get saved language from localStorage or default to 'en'
const savedLocale = localStorage.getItem('locale') || 'en'

export const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: {
    en,
    ar,
    fr,
    it,
    ru
  }
})

export default i18n


# Internationalization (i18n) Setup

This project uses Vue I18n for internationalization support. Currently supports English and Arabic, with the ability to easily add more languages.

## Structure

```
src/i18n/
├── index.ts              # i18n configuration
└── locales/
    ├── en.json          # English translations
    └── ar.json          # Arabic translations
```

## Adding a New Language

### Step 1: Create Translation File

Create a new JSON file in `src/i18n/locales/` with the language code (e.g., `fr.json` for French).

### Step 2: Copy Structure

Copy the structure from `en.json` and translate all the values:

```json
{
  "nav": {
    "home": "Accueil",
    "apartments": "Appartements",
    ...
  }
}
```

### Step 3: Register in i18n/index.ts

Import and add the new language to the messages object:

```typescript
import fr from './locales/fr.json'

export const i18n = createI18n({
  // ...
  messages: {
    en,
    ar,
    fr  // Add here
  }
})
```

### Step 4: Add to Language Store

Update `src/stores/language.ts` to include the new language:

```typescript
const supportedLanguages = [
  { code: 'en', name: 'English', nativeName: 'English', dir: 'ltr' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية', dir: 'rtl' },
  { code: 'fr', name: 'French', nativeName: 'Français', dir: 'ltr' }  // Add here
]
```

**Note:** Set `dir: 'rtl'` for right-to-left languages (Arabic, Hebrew, etc.) and `dir: 'ltr'` for left-to-right languages.

## Using Translations in Components

### In Template

```vue
<template>
  <h1>{{ $t('nav.home') }}</h1>
  <button>{{ $t('common.save') }}</button>
</template>
```

### In Script

```vue
<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const message = t('auth.login.success')
</script>
```

### With Parameters

```json
{
  "validation": {
    "minLength": "Minimum {min} characters required"
  }
}
```

```vue
{{ $t('validation.minLength', { min: 8 }) }}
```

## Language Switcher

The language switcher component is already integrated into the Navbar. It automatically:
- Saves the selected language to localStorage
- Updates the document direction (LTR/RTL)
- Updates all translations throughout the app

## RTL Support

For RTL languages (like Arabic), the app automatically:
- Sets `dir="rtl"` on the HTML element
- Updates the language attribute
- CSS classes should work with Tailwind's RTL support

## Translation Keys Organization

Translations are organized by feature/component:

- `nav.*` - Navigation items
- `auth.*` - Authentication pages
- `apartments.*` - Apartment listings
- `putAnAd.*` - Create listing form
- `common.*` - Common UI elements
- `validation.*` - Form validation messages

## Best Practices

1. **Use descriptive keys**: `auth.login.title` instead of `title1`
2. **Group related translations**: Keep all navigation items under `nav.*`
3. **Avoid hardcoded text**: Always use `$t()` or `t()` for user-facing text
4. **Test RTL layouts**: When adding RTL languages, test the layout thoroughly
5. **Keep translations consistent**: Use the same terminology across the app


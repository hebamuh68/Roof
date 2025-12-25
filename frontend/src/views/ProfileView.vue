<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-24 h-24 mx-auto rounded-full flex items-center justify-center text-white text-3xl font-bold mb-4" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
          {{ userInitials }}
        </div>
        <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2">{{ fullName }}</h1>
        <p class="text-gray-400 capitalize">{{ user?.role }}</p>
      </div>

      <!-- Profile Card -->
      <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 sm:p-8 border border-white border-opacity-10">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Personal Info Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">{{ $t('common.personalInformation') }}</h2>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('profile.firstName') }}</label>
                <input
                  v-model="form.first_name"
                  type="text"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('profile.lastName') }}</label>
                <input
                  v-model="form.last_name"
                  type="text"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>

              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('profile.email') }}</label>
                <input
                  v-model="form.email"
                  type="email"
                  disabled
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-30 border border-gray-700 rounded-xl text-gray-400 cursor-not-allowed"
                />
                <p class="text-xs text-gray-500 mt-1">{{ $t('common.emailCannotChange') }}</p>
              </div>

              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('putAnAd.location') }}</label>
                <input
                  v-model="form.location"
                  type="text"
                  :placeholder="$t('putAnAd.location')"
                  class="w-full px-4 py-3 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Preferences Section -->
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">{{ $t('common.preferences') }}</h2>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('common.flatmatePreferences') }}</label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="pref in flatmateOptions"
                    :key="pref"
                    type="button"
                    @click="toggleFlatmatePref(pref)"
                    :class="[
                      'px-4 py-2 rounded-full text-sm font-medium transition-all',
                      form.flatmate_pref.includes(pref)
                        ? 'text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    ]"
                    :style="form.flatmate_pref.includes(pref) ? { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' } : {}"
                  >
                    {{ pref }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">{{ $t('common.interestsKeywords') }}</label>
                <div class="flex flex-wrap gap-2 mb-2">
                  <span
                    v-for="keyword in form.keywords"
                    :key="keyword"
                    class="inline-flex items-center gap-1 px-3 py-1 bg-secondary-500 bg-opacity-20 text-secondary-300 rounded-full text-sm"
                  >
                    {{ keyword }}
                    <button @click="removeKeyword(keyword)" type="button" class="hover:text-white">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </span>
                </div>
                <div class="flex gap-2">
                  <input
                    v-model="newKeyword"
                    @keyup.enter.prevent="addKeyword"
                    type="text"
                    :placeholder="$t('profile.addKeyword')"
                    class="flex-1 px-4 py-2 bg-gray-800 bg-opacity-50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 transition-all"
                  />
                  <button
                    type="button"
                    @click="addKeyword"
                    class="px-4 py-2 bg-gray-700 text-white rounded-xl hover:bg-gray-600 transition-colors"
                  >
                    {{ $t('common.add') }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <BaseButton
              button-type="submit"
              :loading="saving"
              :label="$t('common.saveChanges')"
              variant="primary"
              size="md"
              class="flex-1"
            />
            <button
              type="button"
              @click="logout"
              class="flex-1 px-8 py-4 bg-red-600 bg-opacity-20 border border-red-500 border-opacity-30 text-red-400 rounded-full font-semibold hover:bg-opacity-30 transition-all"
            >
              {{ $t('common.logout') }}
            </button>
          </div>

          <!-- Error/Success Messages -->
          <p v-if="error" class="text-red-400 text-center">{{ error }}</p>
          <p v-if="success" class="text-green-400 text-center">{{ success }}</p>
        </form>
      </div>

      <!-- Stats Section -->
      <div class="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-xl p-4 text-center border border-white border-opacity-10">
          <div class="text-2xl font-bold text-white">{{ stats.apartments }}</div>
          <div class="text-sm text-gray-400">{{ $t('myApartments.title') }}</div>
        </div>
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-xl p-4 text-center border border-white border-opacity-10">
          <div class="text-2xl font-bold text-white">{{ stats.messages }}</div>
          <div class="text-sm text-gray-400">{{ $t('messages.title') }}</div>
        </div>
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-xl p-4 text-center border border-white border-opacity-10">
          <div class="text-2xl font-bold text-white">{{ stats.views }}</div>
          <div class="text-sm text-gray-400">{{ $t('myApartments.views') }}</div>
        </div>
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-xl p-4 text-center border border-white border-opacity-10">
          <div class="text-2xl font-bold text-white">{{ memberSince }}</div>
          <div class="text-sm text-gray-400">{{ $t('common.memberSince') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useApartmentStore } from '@/stores/apartment'
import { useMessageStore } from '@/stores/message'
import BaseButton from '@/components/buttons/BaseButton.vue'

const { t } = useI18n()

const router = useRouter()
const authStore = useAuthStore()
const apartmentStore = useApartmentStore()
const messageStore = useMessageStore()

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  location: '',
  flatmate_pref: [] as string[],
  keywords: [] as string[]
})

const newKeyword = ref('')
const saving = ref(false)
const error = ref('')
const success = ref('')

const user = computed(() => authStore.user)
const fullName = computed(() => authStore.fullName)
const userInitials = computed(() => {
  if (!user.value) return ''
  return `${user.value.first_name?.charAt(0) || ''}${user.value.last_name?.charAt(0) || ''}`.toUpperCase()
})

const flatmateOptions = computed(() => [
  t('common.clean'),
  t('common.quiet'),
  t('auth.signup.nonSmoker'),
  t('common.earlyRiser'),
  t('common.nightOwl'),
  t('common.social'),
  t('common.petFriendly'),
  t('auth.signup.student'),
  t('common.professional')
])

const stats = computed(() => ({
  apartments: apartmentStore.myApartments.length,
  messages: messageStore.conversations.length,
  views: apartmentStore.myApartments.reduce((sum, a) => sum + (a.view_count || 0), 0)
}))

const memberSince = computed(() => {
  if (!user.value?.created_at) return 'N/A'
  const date = new Date(user.value.created_at)
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
})

const toggleFlatmatePref = (pref: string) => {
  const index = form.flatmate_pref.indexOf(pref)
  if (index > -1) {
    form.flatmate_pref.splice(index, 1)
  } else {
    form.flatmate_pref.push(pref)
  }
}

const addKeyword = () => {
  const keyword = newKeyword.value.trim()
  if (keyword && !form.keywords.includes(keyword)) {
    form.keywords.push(keyword)
    newKeyword.value = ''
  }
}

const removeKeyword = (keyword: string) => {
  form.keywords = form.keywords.filter((k) => k !== keyword)
}

const handleSubmit = async () => {
  saving.value = true
  error.value = ''
  success.value = ''

  try {
    const result = await authStore.updateProfile({
      first_name: form.first_name,
      last_name: form.last_name,
      location: form.location,
      flatmate_pref: form.flatmate_pref,
      keywords: form.keywords
    })

    if (result) {
      success.value = 'Profile updated successfully!'
    } else {
      error.value = authStore.error || 'Failed to update profile'
    }
  } catch (err: any) {
    error.value = err.message || 'Something went wrong'
  } finally {
    saving.value = false
  }
}

const logout = () => {
  authStore.logout()
  router.push({ name: 'home' })
}

// Initialize form with user data
watch(user, (newUser) => {
  if (newUser) {
    form.first_name = newUser.first_name || ''
    form.last_name = newUser.last_name || ''
    form.email = newUser.email || ''
    form.location = newUser.location || ''
    form.flatmate_pref = [...(newUser.flatmate_pref || [])]
    form.keywords = [...(newUser.keywords || [])]
  }
}, { immediate: true })

onMounted(() => {
  apartmentStore.fetchMyApartments()
  messageStore.fetchConversations()
})
</script>

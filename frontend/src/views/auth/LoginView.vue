<template>
  <div class="left-0 right-0 bottom-0 min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-2 sm:p-4 relative overflow-hidden">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute -top-20 -left-20 w-48 h-48 sm:w-72 sm:h-72 rounded-full blur-3xl opacity-20" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute -bottom-20 -right-20 w-48 h-48 sm:w-72 sm:h-72 rounded-full blur-3xl opacity-20" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <div class="relative w-full max-w-sm sm:max-w-md lg:max-w-lg z-10 my-8 sm:my-16 lg:my-20">
      <BaseCard
        :title="$t('auth.login.title')"
        :subtitle="$t('auth.login.subtitle')"
        :success-msg="successMsg"
        :error-msg="errorMsg"
      >
        <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
          <BaseInput
            v-model="formData.email"
            id="email"
            type="email"
            :label="$t('auth.login.email')"
            placeholder="you@example.com"
            required
          />

          <BasePasswordInput
            v-model="formData.password"
            id="password"
            :label="$t('auth.login.password')"
            placeholder="••••••••"
            required
            :minlength="8"
            :maxlength="100"
          />

          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input type="checkbox" v-model="rememberMe" class="w-4 h-4 rounded border-gray-600 bg-gray-700 text-green-500 focus:ring-green-500" />
              <span class="ml-2 text-sm text-gray-300">{{ $t('auth.login.rememberMe') }}</span>
            </label>
            <router-link to="/forgot-password" class="text-sm hover:text-white transition-colors" style="color: #4BC974;">
              {{ $t('auth.login.forgotPassword') }}
            </router-link>
          </div>

          <BaseButton
            button-type="submit"
            :loading="loading"
            :label="loading ? $t('auth.login.loggingIn') : $t('auth.login.loginButton')"
            variant="primary"
            size="md"
            block
          />
        </form>

        <template #footer>
          <div class="mt-4 sm:mt-6 text-center">
            <p class="text-gray-300 text-xs sm:text-sm">
              {{ $t('auth.login.noAccount') }}
              <router-link to="/signup" class="font-semibold hover:text-white transition-colors" style="color: #4BC974;">
                {{ $t('auth.login.signUp') }}
              </router-link>
            </p>
          </div>
        </template>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import BaseButton from '@/components/buttons/BaseButton.vue'
import BaseInput from '@/components/inputs/BaseInput.vue'
import BasePasswordInput from '@/components/inputs/BasePasswordInput.vue'
import BaseCard from '@/components/cards/BaseCard.vue'

const { t } = useI18n()

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()

const formData = reactive({
  email: '',
  password: ''
})

const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')
const rememberMe = ref(false)

const handleLogin = async () => {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  try {
    const success = await authStore.login(formData)

    if (success) {
      successMsg.value = t('auth.login.success')
      uiStore.showSuccess('Welcome back!')

      // Redirect to the intended page or home
      const redirectPath = route.query.redirect as string || '/'
      setTimeout(() => {
        router.push(redirectPath)
      }, 500)
    } else {
      errorMsg.value = authStore.error || 'Login failed. Please check your credentials.'
    }
  } catch (error: any) {
    if (error.response?.data?.detail) {
      if (Array.isArray(error.response.data.detail)) {
        errorMsg.value = error.response.data.detail
          .map((err: any) => err.msg)
          .join('. ')
      } else {
        errorMsg.value = error.response.data.detail
      }
    } else {
      errorMsg.value = 'Something went wrong. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.focus\:border-green-500:focus {
  border-color: #4BC974;
}
</style>

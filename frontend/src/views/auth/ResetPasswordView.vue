<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-2 sm:p-4 relative overflow-hidden">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute -top-20 -left-20 w-48 h-48 sm:w-72 sm:h-72 rounded-full blur-3xl opacity-20" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute -bottom-20 -right-20 w-48 h-48 sm:w-72 sm:h-72 rounded-full blur-3xl opacity-20" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>

    <div class="relative w-full max-w-sm sm:max-w-md lg:max-w-lg z-10 my-8 sm:my-16 lg:my-20">
      <BaseCard
        :title="$t('auth.resetPassword.title')"
        :subtitle="$t('auth.resetPassword.subtitle')"
        :success-msg="successMsg"
        :error-msg="errorMsg"
      >
        <form v-if="!success" @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-5">
          <BasePasswordInput
            v-model="password"
            id="password"
            :label="$t('common.newPassword')"
            placeholder="••••••••"
            required
            :minlength="8"
          />

          <BasePasswordInput
            v-model="confirmPassword"
            id="confirmPassword"
            :label="$t('auth.resetPassword.confirmPassword')"
            placeholder="••••••••"
            required
            :minlength="8"
          />

          <BaseButton
            button-type="submit"
            :loading="loading"
            :disabled="!isValid"
            :label="loading ? $t('auth.resetPassword.resetting') : $t('auth.resetPassword.resetButton')"
            variant="primary"
            size="md"
            block
          />
        </form>

        <div v-else class="text-center py-4">
          <svg class="w-16 h-16 mx-auto mb-4" style="color: #4BC974;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p class="text-gray-300 mb-4">{{ $t('common.passwordResetSuccess') }}</p>
          <router-link to="/login">
            <BaseButton :label="$t('auth.resetPassword.goToLogin')" variant="primary" size="md" />
          </router-link>
        </div>

        <template #footer>
          <div v-if="!success" class="mt-4 sm:mt-6 text-center">
            <router-link to="/login" class="text-gray-300 text-xs sm:text-sm hover:text-white transition-colors" style="color: #4BC974;">
              {{ $t('auth.resetPassword.backToLogin') }}
            </router-link>
          </div>
        </template>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/buttons/BaseButton.vue'
import BasePasswordInput from '@/components/inputs/BasePasswordInput.vue'
import BaseCard from '@/components/cards/BaseCard.vue'

const { t } = useI18n()

const route = useRoute()
const authStore = useAuthStore()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')
const success = ref(false)

const isValid = computed(() => {
  return password.value.length >= 8 && password.value === confirmPassword.value
})

const handleSubmit = async () => {
  if (password.value !== confirmPassword.value) {
    errorMsg.value = t('common.passwordsDoNotMatch')
    return
  }

  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  const token = route.query.token as string
  if (!token) {
    errorMsg.value = t('common.invalidResetToken')
    loading.value = false
    return
  }

  const result = await authStore.confirmPasswordReset(token, password.value)

  if (result) {
    success.value = true
    successMsg.value = t('common.passwordResetSuccessful')
  } else {
    errorMsg.value = authStore.error || t('common.failedResetPassword')
  }

  loading.value = false
}
</script>

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
        :title="$t('auth.forgotPassword.title')"
        :subtitle="$t('auth.forgotPassword.subtitle')"
        :success-msg="successMsg"
        :error-msg="errorMsg"
      >
        <form v-if="!submitted" @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-5">
          <BaseInput
            v-model="email"
            id="email"
            type="email"
            :label="$t('auth.forgotPassword.email')"
            placeholder="you@example.com"
            required
          />

          <BaseButton
            button-type="submit"
            :loading="loading"
            :label="loading ? $t('auth.forgotPassword.sending') : $t('auth.forgotPassword.sendResetLink')"
            variant="primary"
            size="md"
            block
          />
        </form>

        <div v-else class="text-center py-4">
          <svg class="w-16 h-16 mx-auto mb-4" style="color: #4BC974;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          <p class="text-gray-300">{{ $t('common.checkEmail') }}</p>
        </div>

        <template #footer>
          <div class="mt-4 sm:mt-6 text-center">
            <router-link to="/login" class="text-gray-300 text-xs sm:text-sm hover:text-white transition-colors" style="color: #4BC974;">
              {{ $t('auth.forgotPassword.backToLogin') }}
            </router-link>
          </div>
        </template>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/buttons/BaseButton.vue'
import BaseInput from '@/components/inputs/BaseInput.vue'
import BaseCard from '@/components/cards/BaseCard.vue'

const { t } = useI18n()

const authStore = useAuthStore()

const email = ref('')
const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')
const submitted = ref(false)

const handleSubmit = async () => {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  const success = await authStore.requestPasswordReset(email.value)

  if (success) {
    successMsg.value = 'If an account exists with this email, you will receive a reset link.'
    submitted.value = true
  } else {
    // Still show same message to prevent email enumeration
    successMsg.value = 'If an account exists with this email, you will receive a reset link.'
    submitted.value = true
  }

  loading.value = false
}
</script>

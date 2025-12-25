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
        title="Create Account"
        subtitle="Join ROOF - Rental Housing in Egypt"
        :success-msg="successMsg"
        :error-msg="errorMsg"
      >
        <form @submit.prevent="handleSignup" class="space-y-4 sm:space-y-5">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <BaseInput
              v-model="formData.first_name"
              id="first_name"
              type="text"
              label="First Name"
              placeholder="Heba Allah"
              required
              :minlength="2"
              :maxlength="50"
            />

            <BaseInput
              v-model="formData.last_name"
              id="last_name"
              type="text"
              label="Last Name"
              placeholder="Hashim"
              required
              :minlength="2"
              :maxlength="50"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <BaseInput
              v-model="formData.email"
              id="email"
              type="email"
              label="Email"
              placeholder="you@example.com"
              required
            />

            <BasePasswordInput
              v-model="formData.password"
              id="password"
              label="Password"
              placeholder="••••••••"
              required
              :minlength="8"
              :maxlength="100"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <BaseInput
              v-model="formData.location"
              id="location"
              type="text"
              label="Location"
              placeholder="Cairo, Egypt"
              required
              :minlength="2"
              :maxlength="100"
            />

            <BaseSelectInput
              v-model="formData.role"
              id="role"
              label="I want to"
              placeholder="Select role"
              required
            >
              <option value="seeker" class="bg-gray-800">Find an apartment (Seeker)</option>
              <option value="renter" class="bg-gray-800">List my apartment (Renter)</option>
            </BaseSelectInput>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <BaseSelectInput
              v-model="formData.flatmate_pref"
              id="flatmate_pref"
              label="Flatmate Preferences"
              placeholder="Select preferences"
              :multiple="true"
            >
              <option value="non-smoker" class="bg-gray-800">Non-smoker</option>
              <option value="student" class="bg-gray-800">Student</option>
              <option value="pet-friendly" class="bg-gray-800">Pet Friendly</option>
              <option value="quiet" class="bg-gray-800">Quiet</option>
              <option value="party-friendly" class="bg-gray-800">Party Friendly</option>
            </BaseSelectInput>

            <BaseSelectInput
              v-model="formData.keywords"
              id="keywords"
              label="Keywords"
              placeholder="Select keywords"
              :multiple="true"
            >
              <option value="gym" class="bg-gray-800">Gym</option>
              <option value="cooking" class="bg-gray-800">Cooking</option>
              <option value="music" class="bg-gray-800">Music</option>
              <option value="travel" class="bg-gray-800">Travel</option>
              <option value="clean" class="bg-gray-800">Clean</option>
            </BaseSelectInput>
          </div>

          <!-- Role explanation -->
          <div class="p-3 rounded-xl bg-gray-800 bg-opacity-50 border border-gray-700">
            <p v-if="formData.role === 'seeker'" class="text-sm text-gray-300">
              <span class="font-medium text-white">Seeker:</span> Browse and search for apartments. Contact renters to inquire about listings.
            </p>
            <p v-else-if="formData.role === 'renter'" class="text-sm text-gray-300">
              <span class="font-medium text-white">Renter:</span> List your apartments for rent. Manage your listings and communicate with potential tenants.
            </p>
            <p v-else class="text-sm text-gray-400">
              Select a role to see what you can do.
            </p>
          </div>

          <BaseButton
            button-type="submit"
            :loading="loading"
            :label="loading ? 'Creating Account...' : 'Sign Up'"
            variant="primary"
            size="md"
            block
          />
        </form>

        <template #footer>
          <div class="mt-4 sm:mt-6 text-center">
            <p class="text-gray-300 text-xs sm:text-sm">
              Already have an account?
              <router-link to="/login" class="font-semibold hover:text-white transition-colors" style="color: #4BC974;">
                Sign In
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import BaseButton from '@/components/buttons/BaseButton.vue'
import BaseInput from '@/components/inputs/BaseInput.vue'
import BasePasswordInput from '@/components/inputs/BasePasswordInput.vue'
import BaseSelectInput from '@/components/inputs/BaseSelectInput.vue'
import BaseCard from '@/components/cards/BaseCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const formData = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  location: '',
  flatmate_pref: [] as string[],
  keywords: [] as string[],
  role: 'seeker'
})

const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const handleSignup = async () => {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  try {
    const success = await authStore.register(formData)

    if (success) {
      successMsg.value = 'Account created successfully! Redirecting...'
      uiStore.showSuccess('Welcome to ROOF!')

      // Redirect based on role
      setTimeout(() => {
        if (formData.role === 'renter') {
          router.push('/put-an-ad')
        } else {
          router.push('/apartments')
        }
      }, 500)
    } else {
      errorMsg.value = authStore.error || 'Registration failed. Please try again.'
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

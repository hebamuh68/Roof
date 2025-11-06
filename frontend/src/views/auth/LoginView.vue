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
        title="Login"
        subtitle="Login to your ROOF account"
        :success-msg="successMsg"
        :error-msg="errorMsg"
      >
        <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
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

          <BaseButton
            button-type="submit"
            :loading="loading"
            :label="loading ? 'Logging in...' : 'Login'"
            variant="primary"
            size="md"
            block
          />
        </form>

        <template #footer>
          <div class="mt-4 sm:mt-6 text-center">
            <p class="text-gray-300 text-xs sm:text-sm">
              Don't have an account?
              <router-link to="/signup" class="font-semibold hover:text-white transition-colors" style="color: #4BC974;">
                Sign Up
              </router-link>
            </p>
          </div>
        </template>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { loginUser } from "../../services/authService";
import { userLogin, createEmptyUserLogin } from "../../types/userType";
import BaseButton from "../../components/buttons/BaseButton.vue";
import BaseInput from "../../components/inputs/BaseInput.vue";
import BasePasswordInput from "../../components/inputs/BasePasswordInput.vue";
import BaseCard from "../../components/cards/BaseCard.vue";

//================================ Reactive variables ===============================
const formData = reactive<userLogin>(createEmptyUserLogin());

//================================ Methods ===============================
const loading = ref(false);
const successMsg = ref("");
const errorMsg = ref("");

// Submit handler
const handleLogin = async () => {
  loading.value = true;
  successMsg.value = "";
  errorMsg.value = "";

  try {
    const data = await loginUser(formData);
    successMsg.value = data.message || "User logged in successfully!";
    Object.assign(formData, createEmptyUserLogin());
  } catch (error: any) {
    // Handle backend validation errors
    if (error.response?.data?.detail) {
      // If detail is an array (Pydantic validation errors)
      if (Array.isArray(error.response.data.detail)) {
        errorMsg.value = error.response.data.detail
          .map((err: any) => err.msg)
          .join('. ');
      } else {
        // If detail is a string
        errorMsg.value = error.response.data.detail;
      }
    } else {
      errorMsg.value = "Something went wrong. Please try again.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Add custom focus styles */
.focus\:border-green-500:focus {
  border-color: #4BC974;
}
</style>
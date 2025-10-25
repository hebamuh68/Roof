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
      <!-- Main card -->
      <div class="relative bg-white bg-opacity-5 backdrop-blur-xl rounded-2xl sm:rounded-3xl shadow-2xl p-4 sm:p-6 lg:p-8 border border-white border-opacity-10">
        <div class="text-center mb-6 sm:mb-8">
          <h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-2 drop-shadow-lg font-sans">
            Login
          </h2>
          <p class="text-gray-300 text-xs sm:text-sm">Login to your ROOF account</p>
        </div>

        <p v-if="successMsg" class="mb-4 sm:mb-6 rounded-2xl bg-opacity-20 backdrop-blur-sm text-white px-3 sm:px-4 py-2 sm:py-3 text-xs sm:text-sm border border-opacity-30 animate-pulse" style="background-color: rgba(75, 201, 116, 0.2); border-color: rgba(75, 201, 116, 0.3);">
          {{ successMsg }}
        </p>
        
        <p v-if="errorMsg" class="mb-4 sm:mb-6 rounded-2xl bg-red-500 bg-opacity-20 backdrop-blur-sm text-white px-3 sm:px-4 py-2 sm:py-3 text-xs sm:text-sm border border-red-300 border-opacity-30 animate-pulse">
          {{ errorMsg }}
        </p>

        <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
          <div>
            <label for="email" class="block text-xs sm:text-sm font-medium mb-1 sm:mb-2 text-gray-200 drop-shadow">
              Email
            </label>
            <input
              v-model="formData.email"
              id="email"
              type="email"
              required
              class="w-full rounded-lg sm:rounded-xl border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-all duration-300"
              @focus="(e) => e.target.style.boxShadow = '0 0 0 3px rgba(75, 201, 116, 0.1)'"
              @blur="(e) => e.target.style.boxShadow = '0 0 0 0 rgba(75, 201, 116, 0)'"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label for="password" class="block text-xs sm:text-sm font-medium mb-1 sm:mb-2 text-gray-200 drop-shadow">
              Password
            </label>
            <input
              v-model="formData.password"
              id="password"
              type="password"
              required
              minlength="8"
              maxlength="100"
              class="w-full rounded-lg sm:rounded-xl border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-all duration-300"
              @focus="(e) => e.target.style.boxShadow = '0 0 0 3px rgba(75, 201, 116, 0.1)'"
              @blur="(e) => e.target.style.boxShadow = '0 0 0 0 rgba(75, 201, 116, 0)'"
              placeholder="••••••••"
            />
          </div>

           <button
            type="submit"
            :disabled="loading"
            class="w-full rounded-full text-white py-3 sm:py-4 font-bold text-base sm:text-lg shadow-lg hover:shadow-2xl hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 transition-all duration-300 transform"
            style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 sm:mr-3 h-4 w-4 sm:h-5 sm:w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="text-sm sm:text-base">Logging in...</span>
            </span>
            <span v-else class="text-sm sm:text-base">Login</span>
          </button>
        </form>
 
        <div class="mt-4 sm:mt-6 text-center">
          <p class="text-gray-300 text-xs sm:text-sm">
            Don't have an account?
            <router-link to="/signup" class="font-semibold hover:text-white transition-colors" style="color: #4BC974;">
              Sign Up
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { loginUser } from "../../services/authService";
import { userLogin, createEmptyUserLogin } from "../../types/userType";

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
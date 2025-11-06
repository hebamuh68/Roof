<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  successMsg: {
    type: String,
    default: ''
  },
  errorMsg: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <div class="relative bg-white bg-opacity-5 backdrop-blur-xl rounded-2xl sm:rounded-3xl shadow-2xl p-4 sm:p-6 lg:p-8 border border-white border-opacity-10">
    <!-- Header -->
    <div v-if="title || subtitle" class="text-center mb-6 sm:mb-8">
      <h2 v-if="title" class="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-2 drop-shadow-lg font-sans">
        {{ title }}
      </h2>
      <p v-if="subtitle" class="text-gray-300 text-xs sm:text-sm">{{ subtitle }}</p>
    </div>

    <!-- Success Message -->
    <p
      v-if="successMsg"
      class="mb-4 sm:mb-6 rounded-2xl bg-opacity-20 backdrop-blur-sm text-white px-3 sm:px-4 py-2 sm:py-3 text-xs sm:text-sm border border-opacity-30 animate-pulse"
      style="background-color: rgba(75, 201, 116, 0.2); border-color: rgba(75, 201, 116, 0.3);"
    >
      {{ successMsg }}
    </p>

    <!-- Error Message -->
    <p
      v-if="errorMsg"
      class="mb-4 sm:mb-6 rounded-2xl bg-red-500 bg-opacity-20 backdrop-blur-sm text-white px-3 sm:px-4 py-2 sm:py-3 text-xs sm:text-sm border border-red-300 border-opacity-30 animate-pulse"
    >
      {{ errorMsg }}
    </p>

    <!-- Main Content -->
    <slot />

    <!-- Footer -->
    <slot name="footer" />
  </div>
</template>


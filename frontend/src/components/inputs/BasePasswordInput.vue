<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  id: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '••••••••'
  },
  required: {
    type: Boolean,
    default: false
  },
  minlength: {
    type: [Number, String],
    default: undefined
  },
  maxlength: {
    type: [Number, String],
    default: undefined
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: [String, Boolean],
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'focus', 'blur'])

const showPassword = ref(false)
const boxShadowStyle = ref('0 0 0 0 rgba(75, 201, 116, 0)')

const handleInput = (event: Event) => {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
}

const handleFocus = (event: Event) => {
  boxShadowStyle.value = '0 0 0 3px rgba(75, 201, 116, 0.1)'
  emit('focus', event)
}

const handleBlur = (event: Event) => {
  boxShadowStyle.value = '0 0 0 0 rgba(75, 201, 116, 0)'
  emit('blur', event)
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const inputClasses = computed(() => [
  'w-full rounded-lg sm:rounded-xl border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm px-3 sm:px-4 py-2 sm:py-3 pr-10 sm:pr-12 text-sm sm:text-base text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-all duration-300',
  props.error ? 'border-red-500 border-opacity-60' : '',
  props.disabled ? 'opacity-50 cursor-not-allowed' : ''
])
</script>

<template>
  <div class="relative">
    <label
      v-if="label"
      :for="id"
      class="block text-xs sm:text-sm font-medium mb-1 sm:mb-2 text-gray-200 drop-shadow"
    >
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    <div class="relative">
      <input
        :id="id"
        :type="showPassword ? 'text' : 'password'"
        :value="modelValue"
        :placeholder="placeholder"
        :required="required"
        :minlength="minlength"
        :maxlength="maxlength"
        :disabled="disabled"
        :class="inputClasses"
        :style="{ boxShadow: boxShadowStyle }"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        v-bind="$attrs"
      />
      <button
        type="button"
        @click="togglePasswordVisibility"
        class="absolute right-3 sm:right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-300 transition-colors"
        :disabled="disabled"
      >
        <svg
          v-if="showPassword"
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.29 3.29m0 0A9.97 9.97 0 015.12 5.12m3.47 3.47L12 12m-3.41-3.41L5.12 5.12m7.532 7.532L19.29 19.29M12 12l3.41 3.41M12 12l-3.41-3.41m0 0L5.12 5.12"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
          />
        </svg>
      </button>
    </div>
    <p v-if="error && typeof error === 'string'" class="mt-1 text-xs text-red-400">
      {{ error }}
    </p>
  </div>
</template>


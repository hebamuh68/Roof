<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
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
  type: {
    type: String as PropType<'text' | 'email' | 'tel' | 'url' | 'number'>,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
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
  min: {
    type: [Number, String],
    default: undefined
  },
  max: {
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

const inputClasses = computed(() => [
  'w-full rounded-lg sm:rounded-xl border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-all duration-300',
  props.error ? 'border-red-500 border-opacity-60' : '',
  props.disabled ? 'opacity-50 cursor-not-allowed' : ''
])
</script>

<template>
  <div>
    <label
      v-if="label"
      :for="id"
      class="block text-xs sm:text-sm font-medium mb-1 sm:mb-2 text-gray-200 drop-shadow"
    >
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :minlength="minlength"
      :maxlength="maxlength"
      :min="min"
      :max="max"
      :disabled="disabled"
      :class="inputClasses"
      :style="{ boxShadow: boxShadowStyle }"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
      v-bind="$attrs"
    />
    <p v-if="error && typeof error === 'string'" class="mt-1 text-xs text-red-400">
      {{ error }}
    </p>
  </div>
</template>


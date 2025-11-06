<script setup lang="ts">
/**
 * BaseButton Component - Design System
 * 
 * This component provides a unified button system with semantic variants:
 * - primary: Primary actions (green gradient) - create, save, submit, confirm  
 * - secondary: Secondary actions (gray) - cancel, close, dismiss
 * - danger: Destructive actions (red) - delete, remove, destroy
 */
import { computed } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  // Button content
  label: { type: String, default: '' },
  
  // Variant system
  variant: { 
    type: String as PropType<'primary' | 'secondary' | 'danger' | 'ghost' | 'outline'>, 
    default: 'primary' 
  },
  
  // Size system
  size: { 
    type: String as PropType<'sm' | 'md' | 'lg'>, 
    default: 'md' 
  },
  
  // State props
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  
  // Button type
  buttonType: { 
    type: String as PropType<'button' | 'submit' | 'reset'>, 
    default: 'button' 
  },
  
  // Layout
  block: { type: Boolean, default: false },
  
  // Icon support
  icon: { type: Object, default: null },
  iconPosition: { 
    type: String as PropType<'left' | 'right'>, 
    default: 'left' 
  }
})

// Base classes
const baseClasses = computed(() => [
  "flex items-center justify-center gap-2 transition-all duration-300 font-semibold focus:outline-none cursor-pointer",
  "rounded-full",
  props.block ? 'w-full' : 'w-fit'
].filter(Boolean).join(' '))

// Variant styles
const variantClasses = computed(() => {
  const variants = {
    primary: 'text-white shadow-lg hover:-translate-y-1 hover:shadow-2xl backdrop-blur-sm border border-white border-opacity-20 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-lg',
    secondary: 'bg-gray-500 text-white hover:bg-gray-600 active:bg-gray-700 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed',
    danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 active:bg-gray-200 disabled:bg-transparent disabled:text-gray-400 disabled:cursor-not-allowed',
    outline: 'bg-transparent border-2 border-gray-300 text-gray-700 hover:bg-gray-50 active:bg-gray-100 disabled:bg-transparent disabled:text-gray-400 disabled:border-gray-200 disabled:cursor-not-allowed'
  }
  return variants[props.variant] || variants.primary
})

// Primary variant gets the green gradient background
const primaryBackgroundStyle = computed(() => {
  if (props.variant === 'primary' && !props.disabled) {
    return { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' }
  }
  return {}
})

// Size styles
const sizeClasses = computed(() => {
  const sizes = {
    sm: "px-4 py-2 text-sm",
    md: "px-8 py-4 text-lg",
    lg: "px-10 py-5 text-xl"
  }
  return sizes[props.size] || sizes.md
})

// Computed classes
const classes = computed(() => [
  baseClasses.value,
  variantClasses.value,
  sizeClasses.value
].join(' '))

const isDisabled = computed(() => props.loading || props.disabled)
</script>

<template>
  <button
    :type="buttonType"
    :class="classes"
    :style="primaryBackgroundStyle"
    :disabled="isDisabled"
    v-bind="$attrs"
  >
    <!-- Loading state -->
    <template v-if="loading">
      <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span v-if="label">{{ label }}</span>
      <slot v-else />
    </template>
    
    <!-- Normal state -->
    <template v-else>
      <!-- Left icon -->
      <component v-if="icon && iconPosition === 'left'" :is="icon" class="w-5 h-5" />
      
      <!-- Content -->
      <span v-if="label">{{ label }}</span>
      <slot v-else />
      
      <!-- Right icon -->
      <component v-if="icon && iconPosition === 'right'" :is="icon" class="w-5 h-5" />
    </template>
  </button>
</template>

<style scoped>
button {
  transition: background 0.2s, color 0.2s, border 0.2s, transform 0.2s, box-shadow 0.2s;
}
</style>


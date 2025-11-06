<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

interface Option {
  value: string | number
  label: string
}

const props = defineProps({
  modelValue: {
    type: [String, Number, Array] as any,
    default: () => ''
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
    default: 'Select...'
  },
  required: {
    type: Boolean,
    default: false
  },
  multiple: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: [String, Boolean],
    default: false
  },
  options: {
    type: Array as () => Option[],
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'focus', 'blur'])

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const buttonRef = ref<HTMLElement | null>(null)
const hiddenSelectRef = ref<HTMLSelectElement | null>(null)
const searchQuery = ref('')
const boxShadowStyle = ref('0 0 0 0 rgba(75, 201, 116, 0)')
const extractedOptions = ref<Option[]>([])

// Extract options from hidden select element or use props
const extractOptionsFromSelect = (): Option[] => {
  if (!hiddenSelectRef.value) return []
  const options: Option[] = []
  Array.from(hiddenSelectRef.value.options).forEach((option) => {
    if (option.value) {
      options.push({
        value: option.value,
        label: option.text || option.value
      })
    }
  })
  return options
}

// Get options from props or extract from hidden select
const allOptions = computed(() => {
  if (props.options && props.options.length > 0) {
    return props.options
  }
  return extractedOptions.value
})

const filteredOptions = computed(() => {
  if (!searchQuery.value) return allOptions.value
  return allOptions.value.filter(option =>
    option.label.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Get selected values as array
const selectedValues = computed(() => {
  if (props.multiple) {
    return Array.isArray(props.modelValue) ? props.modelValue : []
  }
  return props.modelValue ? [props.modelValue] : []
})

// Display text for single select
const displayText = computed(() => {
  if (props.multiple) {
    const selected = allOptions.value.filter(opt => selectedValues.value.includes(opt.value))
    if (selected.length === 0) return props.placeholder
    if (selected.length === 1) return selected[0].label
    return `${selected.length} selected`
  } else {
    const selected = allOptions.value.find(opt => opt.value === props.modelValue)
    return selected ? selected.label : props.placeholder
  }
})

const isSelected = (value: string | number) => {
  return selectedValues.value.includes(value)
}

const toggleOption = (value: string | number) => {
  if (props.disabled) return

  if (props.multiple) {
    const current = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    const index = current.indexOf(value)
    if (index > -1) {
      current.splice(index, 1)
    } else {
      current.push(value)
    }
    emit('update:modelValue', current)
  } else {
    emit('update:modelValue', value)
    isOpen.value = false
    searchQuery.value = ''
  }
}

const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    searchQuery.value = ''
    emit('focus', new Event('focus'))
  } else {
    emit('blur', new Event('blur'))
  }
}

const closeDropdown = () => {
  isOpen.value = false
  searchQuery.value = ''
  boxShadowStyle.value = '0 0 0 0 rgba(75, 201, 116, 0)'
  emit('blur', new Event('blur'))
}

const handleClickOutside = (event: MouseEvent) => {
  if (
    dropdownRef.value &&
    buttonRef.value &&
    !dropdownRef.value.contains(event.target as Node) &&
    !buttonRef.value.contains(event.target as Node)
  ) {
    closeDropdown()
  }
}

const handleFocus = () => {
  boxShadowStyle.value = '0 0 0 3px rgba(75, 201, 116, 0.1)'
}

const handleBlur = () => {
  if (!isOpen.value) {
    boxShadowStyle.value = '0 0 0 0 rgba(75, 201, 116, 0)'
  }
}

watch(isOpen, (newVal) => {
  if (newVal) {
    handleFocus()
    document.addEventListener('mousedown', handleClickOutside)
  } else {
    document.removeEventListener('mousedown', handleClickOutside)
  }
})

// Watch for changes in hidden select to update options
watch(() => hiddenSelectRef.value, () => {
  if (hiddenSelectRef.value && !props.options?.length) {
    nextTick(() => {
      extractedOptions.value = extractOptionsFromSelect()
    })
  }
}, { immediate: true })

onMounted(() => {
  // Ensure options are extracted after mount
  nextTick(() => {
    if (hiddenSelectRef.value && !props.options?.length) {
      extractedOptions.value = extractOptionsFromSelect()
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})

const buttonClasses = computed(() => [
  'w-full rounded-lg sm:rounded-xl border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base text-white focus:outline-none focus:border-green-500 transition-all duration-300 flex items-center justify-between',
  props.error ? 'border-red-500 border-opacity-60' : '',
  props.disabled ? 'opacity-50 cursor-not-allowed' : '',
  isOpen.value ? 'border-green-500' : ''
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
    
    <div class="relative" ref="buttonRef">
      <button
        type="button"
        :id="id"
        :disabled="disabled"
        :class="buttonClasses"
        :style="{ boxShadow: boxShadowStyle }"
        @click="toggleDropdown"
        @focus="handleFocus"
        @blur="handleBlur"
      >
        <span :class="{ 'text-gray-400': !displayText || displayText === placeholder }">
          {{ displayText }}
        </span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-gray-400 transition-transform duration-200"
          :class="{ 'rotate-180': isOpen }"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      <!-- Dropdown Menu -->
      <Transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          v-if="isOpen"
          ref="dropdownRef"
          class="absolute z-50 w-full mt-1 bg-gray-900 bg-opacity-95 backdrop-blur-sm border-2 border-gray-600 border-opacity-40 rounded-lg sm:rounded-xl shadow-xl max-h-60 overflow-auto"
        >
          <!-- Search input for filtering -->
          <div v-if="allOptions.length > 5" class="p-2 border-b border-gray-600 border-opacity-40">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              class="w-full px-3 py-2 text-sm text-white bg-gray-800 bg-opacity-50 border border-gray-600 border-opacity-40 rounded-lg focus:outline-none focus:border-green-500"
              @click.stop
            />
          </div>

          <!-- Options list -->
          <div class="py-1">
            <button
              v-for="option in filteredOptions"
              :key="option.value"
              type="button"
              @click="toggleOption(option.value)"
              class="w-full px-3 sm:px-4 py-2 sm:py-3 text-left text-sm sm:text-base text-white hover:bg-gray-800 hover:bg-opacity-50 transition-colors flex items-center justify-between"
              :class="{
                'bg-green-500 bg-opacity-20': isSelected(option.value)
              }"
            >
              <span>{{ option.label }}</span>
              <svg
                v-if="isSelected(option.value)"
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-green-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </button>
          </div>

          <!-- No results -->
          <div
            v-if="filteredOptions.length === 0"
            class="px-3 sm:px-4 py-2 sm:py-3 text-sm text-gray-400 text-center"
          >
            No results found
          </div>
        </div>
      </Transition>
    </div>

    <!-- Hidden select to extract options from slot -->
    <select
      v-if="$slots.default"
      ref="hiddenSelectRef"
      class="hidden"
      :multiple="multiple"
    >
      <slot />
    </select>

    <p v-if="multiple" class="text-xs text-gray-400 mt-1">
      Hold Ctrl/Cmd to select multiple
    </p>
    <p v-if="error && typeof error === 'string'" class="mt-1 text-xs text-red-400">
      {{ error }}
    </p>
  </div>
</template>

<style scoped>
/* Custom scrollbar for dropdown */
div::-webkit-scrollbar {
  width: 6px;
}

div::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

div::-webkit-scrollbar-thumb {
  background: rgba(75, 201, 116, 0.5);
  border-radius: 3px;
}

div::-webkit-scrollbar-thumb:hover {
  background: rgba(75, 201, 116, 0.7);
}
</style>

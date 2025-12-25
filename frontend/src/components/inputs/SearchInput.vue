<template>
  <div class="relative" :class="wrapperClasses">
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      type="text"
      :placeholder="$t('common.search')"
      :class="inputClasses"
      :style="inputStyle"
      @focus="handleFocus"
      @blur="handleBlur"
    />
    <SearchIcon :class="iconClasses" />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import SearchIcon from '../icons/search/SearchIcon.vue'

const { t } = useI18n()

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'desktop', // 'desktop' or 'mobile'
    validator: (value) => ['desktop', 'mobile'].includes(value)
  },
  isHomePage: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const boxShadowStyle = ref('0 0 0 0 rgba(75, 201, 116, 0)')

const wrapperClasses = computed(() => {
  if (props.variant === 'desktop') {
    return 'hidden sm:block'
  }
  return ''
})

const inputClasses = computed(() => {
  if (props.variant === 'desktop') {
    return [
      'pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:outline-none text-sm',
      props.isHomePage
        ? 'border-white/30 bg-white/20 text-white placeholder-white/70 focus:ring-white/50'
        : 'border-gray-300 text-gray-700 focus:ring-indigo-500'
    ]
  } else {
    // mobile variant
    return 'w-full pl-10 pr-4 py-3 border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-all duration-300'
  }
})

const inputStyle = computed(() => {
  if (props.variant === 'mobile') {
    return { boxShadow: boxShadowStyle.value }
  }
  return {}
})

const iconClasses = computed(() => {
  if (props.variant === 'desktop') {
    return [
      'h-5 w-5 absolute left-3 top-2.5',
      props.isHomePage ? 'text-white/70' : 'text-gray-400'
    ]
  } else {
    // mobile variant
    return 'h-5 w-5 absolute left-3 top-3.5 text-white/70'
  }
})

const handleFocus = (e) => {
  if (props.variant === 'mobile') {
    boxShadowStyle.value = '0 0 0 3px rgba(75, 201, 116, 0.1)'
  }
}

const handleBlur = (e) => {
  if (props.variant === 'mobile') {
    boxShadowStyle.value = '0 0 0 0 rgba(75, 201, 116, 0)'
  }
}
</script>

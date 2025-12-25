<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  modelValue: File[]
  existingImages?: string[]
  maxFiles?: number
  minFiles?: number
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: File[]): void
  (e: 'remove-existing', index: number): void
}>()

const maxFiles = computed(() => props.maxFiles || 10)
const minFiles = computed(() => props.minFiles || 4)
const dragActive = ref(false)

const previews = computed(() => {
  return props.modelValue.map((file) => URL.createObjectURL(file))
})

const totalImages = computed(() => {
  return (props.existingImages?.length || 0) + props.modelValue.length
})

const canAddMore = computed(() => totalImages.value < maxFiles.value)

const handleDrop = (e: DragEvent) => {
  dragActive.value = false
  const files = e.dataTransfer?.files
  if (files) {
    addFiles(Array.from(files))
  }
}

const handleFileInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files) {
    addFiles(Array.from(target.files))
    target.value = ''
  }
}

const addFiles = (files: File[]) => {
  const validFiles = files.filter((file) => {
    const validTypes = ['image/jpeg', 'image/png', 'image/webp']
    const maxSize = 10 * 1024 * 1024 // 10MB
    return validTypes.includes(file.type) && file.size <= maxSize
  })

  const remaining = maxFiles.value - totalImages.value
  const filesToAdd = validFiles.slice(0, remaining)

  emit('update:modelValue', [...props.modelValue, ...filesToAdd])
}

const removeFile = (index: number) => {
  const newFiles = [...props.modelValue]
  newFiles.splice(index, 1)
  emit('update:modelValue', newFiles)
}

const removeExisting = (index: number) => {
  emit('remove-existing', index)
}

const getExistingImageUrl = (img: string) => {
  if (img.startsWith('http')) return img
  // If URL already has /static/images/ prefix, just prepend base URL
  if (img.startsWith('/static/images/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${img}`
  }
  // Otherwise, add the prefix
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/static/images/${img}`
}
</script>

<template>
  <div class="space-y-4">
    <!-- Upload Area -->
    <div
      @dragover.prevent="dragActive = true"
      @dragleave.prevent="dragActive = false"
      @drop.prevent="handleDrop"
      :class="[
        'relative border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer',
        dragActive
          ? 'border-secondary-500 bg-secondary-500 bg-opacity-10'
          : 'border-gray-600 hover:border-gray-500 bg-gray-800 bg-opacity-30'
      ]"
    >
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp"
        multiple
        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        :disabled="!canAddMore"
        @change="handleFileInput"
      />

      <div class="space-y-2">
        <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        <div class="text-gray-300">
          <span class="font-medium text-secondary-400">Click to upload</span> or drag and drop
        </div>
        <p class="text-sm text-gray-500">
          JPEG, PNG or WebP (max 10MB each)
        </p>
        <p class="text-xs text-gray-500">
          Minimum {{ minFiles }} images required. {{ totalImages }}/{{ maxFiles }} uploaded.
        </p>
      </div>
    </div>

    <!-- Preview Grid -->
    <div v-if="existingImages?.length || modelValue.length" class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <!-- Existing Images -->
      <div
        v-for="(img, index) in existingImages"
        :key="'existing-' + index"
        class="relative group aspect-square rounded-xl overflow-hidden bg-gray-700"
      >
        <img
          :src="getExistingImageUrl(img)"
          :alt="`Image ${index + 1}`"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <button
            @click="removeExisting(index)"
            class="p-2 bg-red-500 rounded-full text-white hover:bg-red-600 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
        <div class="absolute top-2 left-2 px-2 py-0.5 bg-black bg-opacity-50 rounded text-xs text-white">
          Saved
        </div>
      </div>

      <!-- New Uploads -->
      <div
        v-for="(preview, index) in previews"
        :key="'new-' + index"
        class="relative group aspect-square rounded-xl overflow-hidden bg-gray-700"
      >
        <img
          :src="preview"
          :alt="`New image ${index + 1}`"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <button
            @click="removeFile(index)"
            class="p-2 bg-red-500 rounded-full text-white hover:bg-red-600 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
        <div class="absolute top-2 left-2 px-2 py-0.5 bg-secondary-500 bg-opacity-80 rounded text-xs text-white">
          New
        </div>
      </div>
    </div>

    <!-- Validation Message -->
    <p v-if="totalImages < minFiles" class="text-sm text-orange-400">
      Please upload at least {{ minFiles }} images ({{ minFiles - totalImages }} more needed)
    </p>
  </div>
</template>

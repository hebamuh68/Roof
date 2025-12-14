<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">Apartments</h1>
      <p class="text-lg text-gray-600">Browse available apartments in Egypt.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { listApartments } from '../services/apartmentService'
import { onMounted, ref } from 'vue'
import type { apartmentData } from '../types/apartmentType'
const apartments = ref<apartmentData[]>([])

const displayApartments = async () => {
  const response = await listApartments()
  apartments.value = response

  console.log('Loaded apartments:', apartments.value.length)
  console.log(' response.value: ', apartments.value[0])
  console.log('response: ', response)
}

onMounted(() => {
  displayApartments()
})
</script>

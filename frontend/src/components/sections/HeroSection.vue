<template>
  <div class="relative w-screen h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background image with overlay -->
    <img :src="heroBkg" alt="Hero Section" class="w-full h-full object-cover absolute top-0 left-0 z-10 opacity-30" />
    
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10 z-20">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Green accent orbs -->
    <div class="absolute -top-20 -left-20 w-72 h-72 rounded-full blur-3xl opacity-20 z-20" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
    <div class="absolute -bottom-20 -right-20 w-72 h-72 rounded-full blur-3xl opacity-20 z-20" style="background: linear-gradient(90deg, #00A060 0%, #4BC974 100%);"></div>
    
    <!-- Content -->
    <div class="absolute top-32 left-20 sm:left-24 lg:left-32 z-30 text-white max-w-2xl font-poppins">
      <h1 class="text-left text-4xl md:text-6xl lg:text-8xl font-bold mb-4 leading-tight drop-shadow-lg">
        Welcome To <br> ROOF
      </h1>
      <p class="text-lg md:text-base lg:text-xl mb-8 text-left px-4 py-2 relative overflow-hidden text-gray-200 drop-shadow">
        <span class="relative z-10">Rental Housing App In Egypt</span>
      </p>
      <router-link to="/signup">
        <BaseButton label="Get Started" variant="primary" size="md" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import heroBkg from '@/assets/images/heroBkg.png'
import BaseButton from '../buttons/BaseButton.vue'
</script>

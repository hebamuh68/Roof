<template>
  <div class="relative w-screen h-screen overflow-hidden">
    <img :src="heroBkg" alt="Hero Section" class="w-full h-full object-cover absolute top-0 left-0 z-10" />
    <div class="absolute top-32 left-20 sm:left-24 lg:left-32 z-20 text-white max-w-2xl font-poppins">
      <h1 class="text-left text-4xl md:text-6xl lg:text-8xl font-bold mb-4 leading-tight">
        Welcome To <br> ROOF
      </h1>
      <p
        class="text-lg md:text-base lg:text-xl mb-8 text-left px-4 py-2 relative overflow-hidden"
        style="
          background: linear-gradient(90deg, rgba(255,255,255,0.33) 0%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0) 80%);
        "
      >
        <span class="relative z-10">Rental Housing App In Egypt</span>
      </p>
      <button class="text-white px-8 py-4 rounded-full text-lg font-semibold cursor-pointer transition-all duration-300 shadow-lg hover:-translate-y-1 hover:shadow-xl" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
        Get Started
      </button>
    </div>
  </div>
</template>

<script setup>
    import heroBkg from '@/assets/images/heroBkg.png'
</script>

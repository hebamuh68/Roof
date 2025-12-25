<script setup>
import Navbar from './components/common/Navbar.vue'
import ToastContainer from './components/common/ToastContainer.vue'
</script>

<template>
  <Navbar />
  <router-view />
  <ToastContainer />
</template>

<style>
@import '@/assets/base.css';

/* Remove default margins and padding for full-screen layout */
body {
  margin: 0;
  padding: 0;
  background-color: #f0f0f0;
}

#app {
  margin: 0;
  padding: 0;
  min-height: 100vh;
}
</style>

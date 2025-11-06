<script setup>
import Navbar from './components/common/Navbar.vue';
</script>

<template>
  <Navbar/>
  <router-view />
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

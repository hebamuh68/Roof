<template>
  <nav :class="navbarClasses">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left section -->
        <div class="flex items-center gap-8">
          <!-- Logo -->
          <router-link to="/" class="flex items-center space-x-2 cursor-pointer">
            <Logo :class="[
              'h-16 w-16',
              isHomePage ? 'text-white' : 'text-indigo-500'
            ]" />
          </router-link>

          <!-- Navigation Links -->
          <div class="hidden md:flex space-x-12">
            <router-link
              v-for="item in navLinks"
              :key="item.name"
              :to="item.route"
              :class="[
                isActive(item.route)
                  ? isHomePage 
                    ? 'text-white border-b-2 border-white' 
                    : 'text-black border-b-2 border-green-500'
                  : isHomePage
                    ? 'text-white hover:text-gray-200'
                    : 'text-gray-500 hover:text-gray-900',
                'pb-1 text-sm font-medium'
              ]"
            >
              {{ item.name }}
            </router-link>
          </div>
        </div>

        <!-- Right section -->
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search"
              :class="[
                'pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:outline-none text-sm',
                isHomePage 
                  ? 'border-white/30 bg-white/20 text-white placeholder-white/70 focus:ring-white/50' 
                  : 'border-gray-300 text-gray-700 focus:ring-indigo-500'
              ]"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              :class="[
                'h-5 w-5 absolute left-3 top-2.5',
                isHomePage ? 'text-white/70' : 'text-gray-400'
              ]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1116.65 16.65z"
              />
            </svg>
          </div>

          <!-- Login -->
          <router-link to="/login" :class="[
            'p-2 rounded-full',
            isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
          ]">
            Login
          </router-link>
          <!-- Signup -->
          <router-link to="/signup" :class="[
            'p-2 rounded-full',
            isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
          ]">
            Signup
          </router-link>

          <!-- Notification
          <button :class="[
            'p-2 rounded-full',
            isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
          ]">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 00-9.33-4.954M9 21h6"
              />
            </svg>
          </button>
          <!-- User Avatar -->
          <!-- <img
            src="https://randomuser.me/api/portraits/men/32.jpg"
            alt="User Avatar"
            class="h-8 w-8 rounded-full object-cover"
          /> -->
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Logo from './icons/logo.vue'

const route = useRoute()
const searchQuery = ref('')
const navLinks = ref([
  { name: 'Home', route: '/' },
  { name: 'Apartments', route: '/apartments' },
  { name: 'Put an Ad', route: '/put-an-ad' },
  { name: 'About', route: '/about' },
  { name: 'Contact Us', route: '/contact' },
])

const isHomePage = computed(() => route.name === 'home')

const navbarClasses = computed(() => {
  if (isHomePage.value) {
    return 'absolute top-0 left-0 right-0 z-50 bg-transparent'
  }
  return 'bg-white shadow-sm'
})

const isActive = (routePath) => {
  return route.path === routePath
}
</script>

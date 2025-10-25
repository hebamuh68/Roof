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

          <!-- Navigation Links - Desktop -->
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
          <!-- Search - Hidden on mobile -->
          <div class="relative hidden sm:block">
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

          <!-- Auth Links - Hidden on mobile -->
          <div class="hidden sm:flex items-center space-x-4">
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
          </div>

          <!-- Mobile menu button -->
          <button
            @click="toggleMobileMenu"
            :class="[
              'md:hidden p-2 rounded-full',
              isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
            ]"
          >
            <svg
              v-if="!isMobileMenuOpen"
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

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

    <!-- Mobile menu overlay -->
    <div
      v-if="isMobileMenuOpen"
      class="md:hidden fixed inset-0 z-50 bg-black bg-opacity-50"
      @click="closeMobileMenu"
    ></div>

    <!-- Mobile menu -->
    <div
      v-if="isMobileMenuOpen"
      class="md:hidden fixed top-0 right-0 z-50 w-80 h-full bg-gradient-to-br from-gray-900 via-gray-800 to-black backdrop-blur-xl border-l border-white border-opacity-10 transform transition-transform duration-300 ease-in-out"
    >
      <!-- Background pattern overlay -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
      </div>

      <!-- Green accent orb -->
      <div class="absolute -top-20 -left-20 w-48 h-48 rounded-full blur-3xl opacity-20" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"></div>
      
      <div class="relative p-6 h-full flex flex-col">
        <!-- Mobile menu header -->
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-2xl font-bold text-white drop-shadow-lg">
            Menu
          </h2>
          <button
            @click="closeMobileMenu"
            class="p-2 rounded-full text-white/70 hover:text-white hover:bg-white/10 transition-all duration-300"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile search -->
        <div class="mb-6">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search"
              class="w-full pl-10 pr-4 py-3 border-2 border-gray-600 border-opacity-40 bg-gray-900 bg-opacity-40 backdrop-blur-sm rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-all duration-300"
              style="box-shadow: 0 0 0 0 rgba(75, 201, 116, 0);"
              @focus="(e) => e.target.style.boxShadow = '0 0 0 3px rgba(75, 201, 116, 0.1)'"
              @blur="(e) => e.target.style.boxShadow = '0 0 0 0 rgba(75, 201, 116, 0)'"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 absolute left-3 top-3.5 text-white/70"
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
        </div>

        <!-- Mobile navigation links -->
        <div class="space-y-3 mb-8 flex-1">
          <router-link
            v-for="item in navLinks"
            :key="item.name"
            :to="item.route"
            @click="closeMobileMenu"
            :class="[
              'block py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300',
              isActive(item.route)
                ? 'text-white bg-white/20 border border-white/30 shadow-lg'
                : 'text-white/70 hover:text-white hover:bg-white/10 border border-transparent'
            ]"
          >
            {{ item.name }}
          </router-link>
        </div>

        <!-- Mobile auth links -->
        <div class="space-y-3 mt-auto">
          <router-link
            to="/login"
            @click="closeMobileMenu"
            class="block py-3 px-4 rounded-xl text-sm font-medium text-center transition-all duration-300 text-white border border-white/30 hover:bg-white/10"
          >
            Login
          </router-link>
          <router-link
            to="/signup"
            @click="closeMobileMenu"
            class="block py-3 px-4 rounded-xl text-sm font-medium text-center transition-all duration-300 text-white shadow-lg hover:shadow-2xl hover:-translate-y-1 transform"
            style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
          >
            Signup
          </router-link>
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
const isMobileMenuOpen = ref(false)

const navLinks = ref([
  { name: 'Home', route: '/' },
  { name: 'Apartments', route: '/apartments' },
  { name: 'Put an Ad', route: '/put-an-ad' },
  { name: 'About', route: '/about' },
  { name: 'Contact Us', route: '/contact' },
])

const isHomePage = computed(() => route.name === 'home')
const isApartmentsPage = computed(() => route.name === 'apartments')
const isPutAnAdPage = computed(() => route.name === 'putAnAd')
const isAboutPage = computed(() => route.name === 'about')
const isContactPage = computed(() => route.name === 'contact')
const isLoginPage = computed(() => route.name === 'login')
const isSignupPage = computed(() => route.name === 'signup')

const navbarClasses = computed(() => {
  if (isHomePage.value || isApartmentsPage.value || isPutAnAdPage.value || isAboutPage.value || isContactPage.value || isLoginPage.value || isSignupPage.value) {
    return 'absolute top-0 left-0 right-0 z-50 bg-transparent'
  }
  return 'bg-white shadow-sm'
})

const isActive = (routePath) => {
  return route.path === routePath
}

// Mobile menu functions
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

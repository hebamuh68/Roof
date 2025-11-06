<template>
  <nav :class="navbarClasses">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left section -->
        <div class="flex items-center gap-8">
          <!-- Logo -->
          <router-link to="/" class="flex items-center space-x-2 cursor-pointer">
            <img 
              :src="logoImage" 
              alt="Logo" 
              class=" w-10 object-contain"
            />
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
          <SearchInput
            v-model="searchQuery"
            variant="desktop"
            :is-home-page="isHomePage"
          />

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
            <HamburgerIcon
              v-if="!isMobileMenuOpen"
              class="h-6 w-6"
            />
          </button>
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
        </div>

        <!-- Mobile search -->
        <div class="mb-6">
          <SearchInput
            v-model="searchQuery"
            variant="mobile"
          />
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
import SearchInput from '../inputs/SearchInput.vue'
import HamburgerIcon from '../icons/menu/HamburgerIcon.vue'
import logoImage from '../icons/logo.svg'


// ============================== Refs ==============================
const route = useRoute()
const searchQuery = ref('')
const isMobileMenuOpen = ref(false)

// ============================== Computed ==============================
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

// ============================== Methods ==============================
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

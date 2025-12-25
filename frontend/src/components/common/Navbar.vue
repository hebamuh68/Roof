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

          <!-- Authenticated User Menu -->
          <template v-if="isAuthenticated">
            <!-- Notifications -->
            <router-link
              to="/notifications"
              :class="[
                'relative p-2 rounded-full transition-colors',
                isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
              <span
                v-if="unreadNotifications > 0"
                class="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center text-xs font-bold text-white rounded-full"
                style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
              >
                {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
              </span>
            </router-link>

            <!-- Messages -->
            <router-link
              to="/messages"
              :class="[
                'relative p-2 rounded-full transition-colors hidden sm:block',
                isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
              <span
                v-if="unreadMessages > 0"
                class="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center text-xs font-bold text-white rounded-full"
                style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
              >
                {{ unreadMessages > 9 ? '9+' : unreadMessages }}
              </span>
            </router-link>

            <!-- User Dropdown -->
            <div class="relative hidden sm:block">
              <button
                @click="toggleUserMenu"
                :class="[
                  'flex items-center gap-2 p-2 rounded-full transition-colors',
                  isHomePage ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
                ]"
              >
                <div
                  class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium"
                  style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
                >
                  {{ userInitials }}
                </div>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <Transition
                enter-active-class="transition duration-100 ease-out"
                enter-from-class="transform scale-95 opacity-0"
                enter-to-class="transform scale-100 opacity-100"
                leave-active-class="transition duration-75 ease-in"
                leave-from-class="transform scale-100 opacity-100"
                leave-to-class="transform scale-95 opacity-0"
              >
                <div
                  v-if="isUserMenuOpen"
                  class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50"
                >
                  <div class="px-4 py-2 border-b border-gray-100">
                    <p class="text-sm font-medium text-gray-900">{{ user?.first_name }} {{ user?.last_name }}</p>
                    <p class="text-xs text-gray-500">{{ user?.email }}</p>
                  </div>

                  <router-link
                    to="/profile"
                    @click="closeUserMenu"
                    class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                    My Profile
                  </router-link>

                  <router-link
                    to="/my-apartments"
                    @click="closeUserMenu"
                    class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                    </svg>
                    My Apartments
                  </router-link>

                  <router-link
                    v-if="isAdmin"
                    to="/admin"
                    @click="closeUserMenu"
                    class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    Admin Dashboard
                  </router-link>

                  <div class="border-t border-gray-100 mt-2 pt-2">
                    <button
                      @click="handleLogout"
                      class="flex items-center gap-3 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                      </svg>
                      Sign out
                    </button>
                  </div>
                </div>
              </Transition>
            </div>
          </template>

          <!-- Guest Auth Links - Hidden on mobile -->
          <template v-else>
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
          </template>

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

    <!-- User menu backdrop -->
    <div
      v-if="isUserMenuOpen"
      class="fixed inset-0 z-40"
      @click="closeUserMenu"
    ></div>

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

      <div class="relative p-6 h-full flex flex-col overflow-y-auto">
        <!-- Mobile menu header -->
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-2xl font-bold text-white drop-shadow-lg">
            Menu
          </h2>
          <button
            @click="closeMobileMenu"
            class="p-2 text-white/70 hover:text-white rounded-lg"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- User info (if authenticated) -->
        <div v-if="isAuthenticated" class="mb-6 p-4 bg-white/10 rounded-xl">
          <div class="flex items-center gap-3">
            <div
              class="w-12 h-12 rounded-full flex items-center justify-center text-white font-medium"
              style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
            >
              {{ userInitials }}
            </div>
            <div>
              <p class="text-white font-medium">{{ user?.first_name }} {{ user?.last_name }}</p>
              <p class="text-white/60 text-sm">{{ user?.email }}</p>
            </div>
          </div>
        </div>

        <!-- Mobile search -->
        <div class="mb-6">
          <SearchInput
            v-model="searchQuery"
            variant="mobile"
          />
        </div>

        <!-- Mobile navigation links -->
        <div class="space-y-3 mb-6 flex-1">
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

          <!-- Authenticated mobile links -->
          <template v-if="isAuthenticated">
            <div class="h-px bg-white/20 my-4"></div>

            <router-link
              to="/notifications"
              @click="closeMobileMenu"
              class="flex items-center justify-between py-3 px-4 rounded-xl text-sm font-medium text-white/70 hover:text-white hover:bg-white/10 border border-transparent"
            >
              <span>Notifications</span>
              <span
                v-if="unreadNotifications > 0"
                class="px-2 py-0.5 text-xs font-bold text-white rounded-full"
                style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
              >
                {{ unreadNotifications }}
              </span>
            </router-link>

            <router-link
              to="/messages"
              @click="closeMobileMenu"
              class="flex items-center justify-between py-3 px-4 rounded-xl text-sm font-medium text-white/70 hover:text-white hover:bg-white/10 border border-transparent"
            >
              <span>Messages</span>
              <span
                v-if="unreadMessages > 0"
                class="px-2 py-0.5 text-xs font-bold text-white rounded-full"
                style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
              >
                {{ unreadMessages }}
              </span>
            </router-link>

            <router-link
              to="/profile"
              @click="closeMobileMenu"
              class="block py-3 px-4 rounded-xl text-sm font-medium text-white/70 hover:text-white hover:bg-white/10 border border-transparent"
            >
              My Profile
            </router-link>

            <router-link
              to="/my-apartments"
              @click="closeMobileMenu"
              class="block py-3 px-4 rounded-xl text-sm font-medium text-white/70 hover:text-white hover:bg-white/10 border border-transparent"
            >
              My Apartments
            </router-link>

            <router-link
              v-if="isAdmin"
              to="/admin"
              @click="closeMobileMenu"
              class="block py-3 px-4 rounded-xl text-sm font-medium text-white/70 hover:text-white hover:bg-white/10 border border-transparent"
            >
              Admin Dashboard
            </router-link>
          </template>
        </div>

        <!-- Mobile auth links -->
        <div class="space-y-3 mt-auto">
          <template v-if="isAuthenticated">
            <button
              @click="handleMobileLogout"
              class="w-full py-3 px-4 rounded-xl text-sm font-medium text-center transition-all duration-300 text-red-400 border border-red-400/30 hover:bg-red-500/10"
            >
              Sign out
            </button>
          </template>
          <template v-else>
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
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'
import { useMessageStore } from '@/stores/message'
import SearchInput from '../inputs/SearchInput.vue'
import HamburgerIcon from '../icons/menu/HamburgerIcon.vue'
import logoImage from '../icons/logo.svg'


// ============================== Stores ==============================
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const messageStore = useMessageStore()

// ============================== Refs ==============================
const searchQuery = ref('')
const isMobileMenuOpen = ref(false)
const isUserMenuOpen = ref(false)

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

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)

const userInitials = computed(() => {
  if (!user.value) return ''
  return `${user.value.first_name?.charAt(0) || ''}${user.value.last_name?.charAt(0) || ''}`.toUpperCase()
})

const unreadNotifications = computed(() => notificationStore.unreadCount)
const unreadMessages = computed(() => messageStore.unreadCount)

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

// User menu functions
const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const closeUserMenu = () => {
  isUserMenuOpen.value = false
}

const handleLogout = async () => {
  closeUserMenu()
  await authStore.logout()
  router.push('/')
}

const handleMobileLogout = async () => {
  closeMobileMenu()
  await authStore.logout()
  router.push('/')
}

// Fetch notifications and messages on mount if authenticated
onMounted(() => {
  if (authStore.isAuthenticated) {
    notificationStore.fetchNotifications()
    messageStore.fetchConversations()
  }
})

// Close menus on route change
const unwatch = router.afterEach(() => {
  closeUserMenu()
  closeMobileMenu()
})

onUnmounted(() => {
  unwatch()
})
</script>

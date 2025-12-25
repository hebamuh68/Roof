<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2">{{ $t('admin.dashboard.title') }}</h1>
        <p class="text-gray-400">{{ $t('common.platformOverview') }}</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-400">Total</span>
          </div>
          <div class="text-3xl font-bold text-white mb-1">{{ stats.total_users }}</div>
          <div class="text-sm text-gray-400">Users</div>
        </div>

        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 rounded-xl bg-blue-500 bg-opacity-20 flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <span class="text-xs text-gray-400">Total</span>
          </div>
          <div class="text-3xl font-bold text-white mb-1">{{ stats.total_apartments }}</div>
          <div class="text-sm text-gray-400">Apartments</div>
        </div>

        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 rounded-xl bg-green-500 bg-opacity-20 flex items-center justify-center">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-400">Active</span>
          </div>
          <div class="text-3xl font-bold text-white mb-1">{{ stats.active_apartments }}</div>
          <div class="text-sm text-gray-400">Active Listings</div>
        </div>

        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 rounded-xl bg-purple-500 bg-opacity-20 flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-400">Seekers</span>
          </div>
          <div class="text-3xl font-bold text-white mb-1">{{ stats.seekers || stats.users_by_role?.seeker || 0 }}</div>
          <div class="text-sm text-gray-400">Seekers</div>
        </div>
      </div>

      <!-- Distribution Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Users by Role -->
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
          <h3 class="text-lg font-semibold text-white mb-4">{{ $t('common.usersByRole') }}</h3>
          <div class="space-y-4">
            <div v-for="(count, role) in stats.users_by_role" :key="role">
              <div class="flex items-center justify-between mb-1">
                <span class="text-gray-300 capitalize">{{ role }}</span>
                <span class="text-white font-medium">{{ count }}</span>
              </div>
              <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :style="{
                    width: `${(count / stats.total_users) * 100}%`,
                    background: getRoleColor(role)
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Apartments by Status -->
        <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
          <h3 class="text-lg font-semibold text-white mb-4">{{ $t('common.apartmentsByStatus') }}</h3>
          <div class="space-y-4">
            <div v-for="(count, status) in stats.apartments_by_status" :key="status">
              <div class="flex items-center justify-between mb-1">
                <span class="text-gray-300 capitalize">{{ status }}</span>
                <span class="text-white font-medium">{{ count }}</span>
              </div>
              <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :style="{
                    width: `${(count / stats.total_apartments) * 100}%`,
                    background: getStatusColor(status)
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-10">
        <h3 class="text-lg font-semibold text-white mb-4">Quick Actions</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link
            to="/admin/users"
            class="flex items-center gap-4 p-4 bg-gray-800 bg-opacity-50 rounded-xl hover:bg-opacity-70 transition-colors"
          >
            <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
            <div>
              <div class="font-medium text-white">Manage Users</div>
              <div class="text-sm text-gray-400">View and manage all users</div>
            </div>
          </router-link>

          <router-link
            to="/apartments"
            class="flex items-center gap-4 p-4 bg-gray-800 bg-opacity-50 rounded-xl hover:bg-opacity-70 transition-colors"
          >
            <div class="w-10 h-10 rounded-lg bg-blue-500 bg-opacity-20 flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <div>
              <div class="font-medium text-white">{{ $t('admin.apartments.viewApartments') }}</div>
              <div class="text-sm text-gray-400">{{ $t('common.browseAllListings') }}</div>
            </div>
          </router-link>

          <button
            @click="refreshStats"
            class="flex items-center gap-4 p-4 bg-gray-800 bg-opacity-50 rounded-xl hover:bg-opacity-70 transition-colors"
          >
            <div class="w-10 h-10 rounded-lg bg-purple-500 bg-opacity-20 flex items-center justify-center">
              <svg :class="['w-5 h-5 text-purple-400', refreshing ? 'animate-spin' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </div>
            <div>
              <div class="font-medium text-white">{{ $t('admin.dashboard.refreshStats') }}</div>
              <div class="text-sm text-gray-400">{{ $t('common.updateDashboard') }}</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'

const { t } = useI18n()

const stats = reactive({
  total_users: 0,
  total_apartments: 0,
  active_apartments: 0,
  seekers: 0,
  renters: 0,
  users_by_role: {
    seeker: 0,
    renter: 0,
    admin: 0
  },
  apartments_by_status: {
    draft: 0,
    published: 0,
    archived: 0
  }
})

const loading = ref(true)
const refreshing = ref(false)

const getRoleColor = (role: string) => {
  const colors: Record<string, string> = {
    seeker: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)',
    renter: 'linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%)',
    admin: 'linear-gradient(90deg, #F59E0B 0%, #D97706 100%)'
  }
  return colors[role] || 'linear-gradient(90deg, #6B7280 0%, #4B5563 100%)'
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    published: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)',
    draft: 'linear-gradient(90deg, #F59E0B 0%, #D97706 100%)',
    archived: 'linear-gradient(90deg, #6B7280 0%, #4B5563 100%)'
  }
  return colors[status] || 'linear-gradient(90deg, #6B7280 0%, #4B5563 100%)'
}

const fetchStats = async () => {
  try {
    const response = await api.get('/admin/stats')
    Object.assign(stats, response.data)
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  } finally {
    loading.value = false
  }
}

const refreshStats = async () => {
  refreshing.value = true
  await fetchStats()
  refreshing.value = false
}

onMounted(() => {
  fetchStats()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <router-link to="/admin" class="text-gray-400 hover:text-white transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </router-link>
            <h1 class="text-3xl sm:text-4xl font-bold text-white">{{ $t('admin.users.title') }}</h1>
          </div>
          <p class="text-gray-400">{{ $t('common.manageAllUsers') }}</p>
        </div>

        <!-- Search -->
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$t('admin.users.searchUsers')"
            class="w-full sm:w-64 px-4 py-2 pl-10 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500"
          />
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
        <button
          v-for="role in roleFilters"
          :key="role.value"
          @click="activeRole = role.value"
          :class="[
            'px-4 py-2 rounded-xl font-medium transition-all whitespace-nowrap',
            activeRole === role.value
              ? 'text-white'
              : 'bg-white bg-opacity-10 text-gray-300 hover:bg-opacity-20'
          ]"
          :style="activeRole === role.value ? { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' } : {}"
        >
          {{ role.label }}
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="bg-white bg-opacity-5 rounded-xl p-4 animate-pulse">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-gray-700 rounded-full"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-700 rounded w-1/4"></div>
              <div class="h-3 bg-gray-700 rounded w-1/3"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredUsers.length === 0" class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
        </svg>
        <h3 class="text-xl font-medium text-white mb-2">{{ $t('common.noUsersFound') }}</h3>
        <p class="text-gray-400">{{ $t('common.tryAdjustingSearch') }}</p>
      </div>

      <!-- Users Table -->
      <div v-else class="bg-white bg-opacity-5 backdrop-blur-sm rounded-2xl border border-white border-opacity-10 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white border-opacity-10">
                <th class="px-6 py-4 text-left text-sm font-medium text-gray-400">{{ $t('common.user') }}</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-gray-400">{{ $t('common.email') }}</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-gray-400">{{ $t('common.role') }}</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-gray-400">{{ $t('putAnAd.location') }}</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-gray-400">{{ $t('common.joined') }}</th>
                <th class="px-6 py-4 text-right text-sm font-medium text-gray-400">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="user in filteredUsers"
                :key="user.id"
                class="border-b border-white border-opacity-5 hover:bg-white hover:bg-opacity-5 transition-colors"
              >
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-medium" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
                      {{ getInitials(user) }}
                    </div>
                    <div>
                      <div class="font-medium text-white">{{ user.first_name }} {{ user.last_name }}</div>
                      <div class="text-sm text-gray-400">ID: {{ user.id }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-gray-300">{{ user.email }}</td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium',
                      getRoleClass(user.role)
                    ]"
                  >
                    {{ user.role }}
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-300">{{ user.location || '-' }}</td>
                <td class="px-6 py-4 text-gray-400 text-sm">{{ formatDate(user.created_at) }}</td>
                <td class="px-6 py-4 text-right">
                  <button
                    @click="confirmDelete(user)"
                    class="p-2 text-red-400 hover:bg-red-500 hover:bg-opacity-20 rounded-lg transition-colors"
                    :title="$t('messages.deleteUser')"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div
        v-if="showDeleteModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        @click="showDeleteModal = false"
      >
        <div
          class="bg-gray-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-gray-700"
          @click.stop
        >
          <h3 class="text-xl font-semibold text-white mb-2">{{ $t('admin.users.deleteUser') }}</h3>
          <p class="text-gray-400 mb-6">
            {{ $t('admin.users.deleteConfirmation', { name: `${userToDelete?.first_name} ${userToDelete?.last_name}` }) }}
          </p>
          <div class="flex gap-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 bg-gray-700 text-white rounded-xl font-medium hover:bg-gray-600 transition-colors"
            >
              {{ $t('common.cancel') }}
            </button>
            <button
              @click="deleteUser"
              :disabled="deleting"
              class="flex-1 px-4 py-2 bg-red-600 text-white rounded-xl font-medium hover:bg-red-700 transition-colors disabled:opacity-50"
            >
              {{ deleting ? $t('common.deleting') : $t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'
import { useUIStore } from '@/stores/ui'
import type { User } from '@/types'

const { t } = useI18n()

const uiStore = useUIStore()

const users = ref<User[]>([])
const loading = ref(true)
const searchQuery = ref('')
const activeRole = ref('all')
const showDeleteModal = ref(false)
const userToDelete = ref<User | null>(null)
const deleting = ref(false)

const roleFilters = computed(() => [
  { value: 'all', label: t('common.allUsers') },
  { value: 'seeker', label: t('common.seekers') },
  { value: 'renter', label: t('common.renters') },
  { value: 'admin', label: t('common.admins') }
])

const filteredUsers = computed(() => {
  let result = users.value

  // Filter by role
  if (activeRole.value !== 'all') {
    result = result.filter((u) => u.role === activeRole.value)
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(
      (u) =>
        u.first_name?.toLowerCase().includes(query) ||
        u.last_name?.toLowerCase().includes(query) ||
        u.email?.toLowerCase().includes(query)
    )
  }

  return result
})

const getInitials = (user: User) => {
  return `${user.first_name?.charAt(0) || ''}${user.last_name?.charAt(0) || ''}`.toUpperCase()
}

const getRoleClass = (role: string) => {
  switch (role) {
    case 'admin':
      return 'bg-orange-500 bg-opacity-20 text-orange-300'
    case 'renter':
      return 'bg-blue-500 bg-opacity-20 text-blue-300'
    case 'seeker':
      return 'bg-secondary-500 bg-opacity-20 text-secondary-300'
    default:
      return 'bg-gray-500 bg-opacity-20 text-gray-300'
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await api.get('/admin/users')
    users.value = response.data
  } catch (error) {
    console.error(t('common.failedFetchUsers'), error)
    uiStore.showError(t('common.failedFetchUsers'))
  } finally {
    loading.value = false
  }
}

const confirmDelete = (user: User) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const deleteUser = async () => {
  if (!userToDelete.value) return

  deleting.value = true
  try {
    await api.delete(`/admin/users/${userToDelete.value.id}`)
    users.value = users.value.filter((u) => u.id !== userToDelete.value?.id)
    uiStore.showSuccess(t('common.userDeleted'))
    showDeleteModal.value = false
    userToDelete.value = null
  } catch (error) {
    console.error(t('common.failedDeleteUser'), error)
    uiStore.showError(t('common.failedDeleteUser'))
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

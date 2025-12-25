// stores/admin.ts - Admin store
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User, PlatformStats } from '@/types'
import api from '@/services/api'

export const useAdminStore = defineStore('admin', () => {
  // State
  const users = ref<User[]>([])
  const stats = ref<PlatformStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Fetch platform statistics
  const fetchStats = async (): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await api.get<PlatformStats>('/admin/stats')
      stats.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch statistics'
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch all users
  const fetchUsers = async (skip = 0, limit = 100): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await api.get<User[]>(`/admin/users?skip=${skip}&limit=${limit}`)
      users.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch users'
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete user
  const deleteUser = async (userId: number): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      await api.delete(`/admin/users/${userId}`)
      users.value = users.value.filter((u) => u.id !== userId)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete user'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    users,
    stats,
    loading,
    error,
    // Actions
    fetchStats,
    fetchUsers,
    deleteUser
  }
})

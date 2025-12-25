// stores/notification.ts - Notification store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Notification } from '@/types'
import api from '@/services/api'

export const useNotificationStore = defineStore('notification', () => {
  // State
  const notifications = ref<Notification[]>([])
  const unreadCount = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const hasUnreadNotifications = computed(() => unreadCount.value > 0)
  const unreadNotifications = computed(() => notifications.value.filter((n) => !n.is_read))
  const sortedNotifications = computed(() =>
    [...notifications.value].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  )

  // Fetch notifications (backend uses skip/limit)
  const fetchNotifications = async (skip = 0, limit = 50, unreadOnly = false): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams({
        skip: skip.toString(),
        limit: limit.toString(),
        unread_only: unreadOnly.toString()
      })
      const response = await api.get<{ notifications: Notification[]; total: number; unread_count: number }>(
        `/notifications/?${params}`
      )
      notifications.value = response.data.notifications || response.data.items || response.data
      if (response.data.unread_count !== undefined) {
        unreadCount.value = response.data.unread_count
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch notifications'
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch unread count
  const fetchUnreadCount = async (): Promise<void> => {
    try {
      const response = await api.get<{ unread_count: number }>('/notifications/unread-count')
      unreadCount.value = response.data.unread_count
    } catch (err) {
      // Silent fail for badge count
    }
  }

  // Mark single notification as read
  const markAsRead = async (id: number): Promise<boolean> => {
    try {
      await api.patch(`/notifications/${id}/read`)

      // Update local state
      const index = notifications.value.findIndex((n) => n.id === id)
      if (index !== -1) {
        notifications.value[index].is_read = true
      }
      unreadCount.value = Math.max(0, unreadCount.value - 1)

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to mark as read'
      return false
    }
  }

  // Mark all or specific notifications as read
  const markAllAsRead = async (ids?: number[]): Promise<boolean> => {
    try {
      await api.patch('/notifications/mark-read', { notification_ids: ids })

      // Update local state
      if (ids) {
        notifications.value = notifications.value.map((n) => {
          if (ids.includes(n.id)) {
            return { ...n, is_read: true }
          }
          return n
        })
        unreadCount.value = Math.max(0, unreadCount.value - ids.length)
      } else {
        notifications.value = notifications.value.map((n) => ({ ...n, is_read: true }))
        unreadCount.value = 0
      }

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to mark as read'
      return false
    }
  }

  // Delete notification
  const deleteNotification = async (id: number): Promise<boolean> => {
    try {
      await api.delete(`/notifications/${id}`)
      const notification = notifications.value.find((n) => n.id === id)
      notifications.value = notifications.value.filter((n) => n.id !== id)
      if (notification && !notification.is_read) {
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete notification'
      return false
    }
  }

  // Delete all notifications
  const deleteAllNotifications = async (readOnly = false): Promise<boolean> => {
    try {
      await api.delete(`/notifications/?read_only=${readOnly}`)
      if (readOnly) {
        notifications.value = notifications.value.filter((n) => !n.is_read)
      } else {
        notifications.value = []
        unreadCount.value = 0
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete notifications'
      return false
    }
  }

  return {
    // State
    notifications,
    unreadCount,
    loading,
    error,
    // Getters
    hasUnreadNotifications,
    unreadNotifications,
    sortedNotifications,
    // Actions
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    deleteAllNotifications
  }
})

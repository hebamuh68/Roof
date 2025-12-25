<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2">Notifications</h1>
          <p class="text-gray-400">
            <span v-if="unreadCount > 0">{{ unreadCount }} unread</span>
            <span v-else>All caught up!</span>
          </p>
        </div>

        <div class="flex gap-3">
          <button
            v-if="unreadCount > 0"
            @click="markAllRead"
            class="px-4 py-2 bg-white bg-opacity-10 text-white rounded-xl font-medium hover:bg-opacity-20 transition-colors"
          >
            Mark all as read
          </button>
          <button
            v-if="notifications.length > 0"
            @click="showClearModal = true"
            class="px-4 py-2 bg-white bg-opacity-10 text-gray-300 rounded-xl font-medium hover:bg-opacity-20 transition-colors"
          >
            Clear all
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="bg-white bg-opacity-5 rounded-xl p-4 animate-pulse">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 bg-gray-700 rounded-full"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-700 rounded w-3/4"></div>
              <div class="h-3 bg-gray-700 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="notifications.length === 0" class="text-center py-16">
        <svg class="w-20 h-20 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
        </svg>
        <h3 class="text-xl font-medium text-white mb-2">No notifications</h3>
        <p class="text-gray-400">You're all caught up!</p>
      </div>

      <!-- Notifications List -->
      <div v-else class="space-y-3">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'bg-white bg-opacity-5 backdrop-blur-sm rounded-xl p-4 border border-white transition-all cursor-pointer',
            notification.is_read ? 'border-opacity-5' : 'border-opacity-20 bg-opacity-10'
          ]"
          @click="handleNotificationClick(notification)"
        >
          <div class="flex items-start gap-4">
            <!-- Icon -->
            <div
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0',
                getNotificationIconClass(notification.type)
              ]"
            >
              <svg v-if="notification.type === 'message'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
              <svg v-else-if="notification.type === 'inquiry'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <div>
                  <h3 :class="['font-medium', notification.is_read ? 'text-gray-300' : 'text-white']">
                    {{ notification.title }}
                  </h3>
                  <p class="text-sm text-gray-400 mt-1">{{ notification.content }}</p>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-2 flex-shrink-0">
                  <span class="text-xs text-gray-500">{{ formatTime(notification.created_at) }}</span>
                  <button
                    @click.stop="deleteNotification(notification.id)"
                    class="p-1 hover:bg-white hover:bg-opacity-10 rounded-lg transition-colors"
                  >
                    <svg class="w-4 h-4 text-gray-500 hover:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Unread indicator -->
              <div v-if="!notification.is_read" class="mt-2">
                <span class="inline-block w-2 h-2 rounded-full bg-secondary-500"></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Clear Modal -->
      <div
        v-if="showClearModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        @click="showClearModal = false"
      >
        <div
          class="bg-gray-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-gray-700"
          @click.stop
        >
          <h3 class="text-xl font-semibold text-white mb-2">Clear Notifications</h3>
          <p class="text-gray-400 mb-6">What would you like to clear?</p>
          <div class="space-y-3">
            <button
              @click="clearAll(true)"
              class="w-full px-4 py-3 bg-gray-700 text-white rounded-xl font-medium hover:bg-gray-600 transition-colors text-left"
            >
              Clear read notifications only
            </button>
            <button
              @click="clearAll(false)"
              class="w-full px-4 py-3 bg-red-600 text-white rounded-xl font-medium hover:bg-red-700 transition-colors text-left"
            >
              Clear all notifications
            </button>
            <button
              @click="showClearModal = false"
              class="w-full px-4 py-3 border border-gray-600 text-gray-300 rounded-xl font-medium hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notification'
import { useUIStore } from '@/stores/ui'
import type { Notification } from '@/types'

const router = useRouter()
const notificationStore = useNotificationStore()
const uiStore = useUIStore()

const showClearModal = ref(false)

const notifications = computed(() => notificationStore.sortedNotifications)
const loading = computed(() => notificationStore.loading)
const unreadCount = computed(() => notificationStore.unreadCount)

const getNotificationIconClass = (type: string) => {
  switch (type) {
    case 'message':
      return 'bg-blue-500 bg-opacity-20 text-blue-400'
    case 'inquiry':
      return 'bg-secondary-500 bg-opacity-20 text-secondary-400'
    default:
      return 'bg-gray-500 bg-opacity-20 text-gray-400'
  }
}

const formatTime = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m`
  if (diffHours < 24) return `${diffHours}h`
  if (diffDays < 7) return `${diffDays}d`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const handleNotificationClick = async (notification: Notification) => {
  // Mark as read
  if (!notification.is_read) {
    await notificationStore.markAsRead(notification.id)
  }

  // Navigate based on type
  if (notification.type === 'message' && notification.data?.sender_id) {
    router.push({ name: 'conversation', params: { userId: notification.data.sender_id } })
  } else if (notification.type === 'inquiry' && notification.data?.apartment_id) {
    router.push({ name: 'apartmentDetail', params: { id: notification.data.apartment_id } })
  }
}

const markAllRead = async () => {
  await notificationStore.markAllAsRead()
  uiStore.showSuccess('All notifications marked as read')
}

const deleteNotification = async (id: number) => {
  await notificationStore.deleteNotification(id)
}

const clearAll = async (readOnly: boolean) => {
  await notificationStore.deleteAllNotifications(readOnly)
  showClearModal.value = false
  uiStore.showSuccess(readOnly ? 'Read notifications cleared' : 'All notifications cleared')
}

onMounted(() => {
  notificationStore.fetchNotifications()
})
</script>

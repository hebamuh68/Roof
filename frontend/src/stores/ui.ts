// stores/ui.ts - UI state store (toasts, modals, loading)
import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  duration: number
}

export const useUIStore = defineStore('ui', () => {
  // State
  const toasts = ref<Toast[]>([])
  const globalLoading = ref(false)
  const sidebarOpen = ref(false)
  let toastId = 0

  // Add toast
  const showToast = (
    message: string,
    type: Toast['type'] = 'info',
    duration = 4000
  ): number => {
    const id = ++toastId
    const toast: Toast = { id, message, type, duration }

    toasts.value.push(toast)

    // Auto remove
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }

  // Convenience methods
  const showSuccess = (message: string, duration = 4000) =>
    showToast(message, 'success', duration)

  const showError = (message: string, duration = 5000) =>
    showToast(message, 'error', duration)

  const showWarning = (message: string, duration = 4000) =>
    showToast(message, 'warning', duration)

  const showInfo = (message: string, duration = 4000) =>
    showToast(message, 'info', duration)

  // Remove toast
  const removeToast = (id: number) => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  // Clear all toasts
  const clearToasts = () => {
    toasts.value = []
  }

  // Global loading
  const setGlobalLoading = (loading: boolean) => {
    globalLoading.value = loading
  }

  // Sidebar
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const closeSidebar = () => {
    sidebarOpen.value = false
  }

  return {
    // State
    toasts,
    globalLoading,
    sidebarOpen,
    // Actions
    showToast,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    removeToast,
    clearToasts,
    setGlobalLoading,
    toggleSidebar,
    closeSidebar
  }
})

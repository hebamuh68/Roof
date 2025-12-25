// stores/message.ts - Messaging store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Message, Conversation, SendMessageData } from '@/types'
import api from '@/services/api'

export const useMessageStore = defineStore('message', () => {
  // State
  const conversations = ref<Conversation[]>([])
  const currentConversation = ref<Message[]>([])
  const currentOtherUserId = ref<number | null>(null)
  const unreadCount = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const hasUnreadMessages = computed(() => unreadCount.value > 0)
  const sortedConversations = computed(() =>
    [...conversations.value].sort(
      (a, b) =>
        new Date(b.last_message.created_at).getTime() -
        new Date(a.last_message.created_at).getTime()
    )
  )

  // Fetch all conversations
  const fetchConversations = async (): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await api.get<Conversation[]>('/messages/conversations')
      conversations.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch conversations'
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch conversation thread (backend uses skip/limit)
  const fetchConversation = async (
    otherUserId: number,
    skip = 0,
    limit = 50
  ): Promise<boolean> => {
    loading.value = true
    error.value = null
    currentOtherUserId.value = otherUserId

    try {
      const response = await api.get<Message[]>(
        `/messages/conversation/${otherUserId}?skip=${skip}&limit=${limit}`
      )
      currentConversation.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch conversation'
      return false
    } finally {
      loading.value = false
    }
  }

  // Send message
  const sendMessage = async (data: SendMessageData): Promise<Message | null> => {
    loading.value = true
    error.value = null

    try {
      const response = await api.post<Message>('/messages/send', data)
      const newMessage = response.data

      // Add to current conversation if viewing
      if (currentOtherUserId.value === data.receiver_id) {
        currentConversation.value.push(newMessage)
      }

      // Update conversation list
      await fetchConversations()

      // Update unread count
      await fetchUnreadCount()

      return newMessage
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to send message'
      return null
    } finally {
      loading.value = false
    }
  }

  // Delete message
  const deleteMessage = async (messageId: number): Promise<boolean> => {
    try {
      await api.delete(`/messages/${messageId}`)
      currentConversation.value = currentConversation.value.filter((m) => m.id !== messageId)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete message'
      return false
    }
  }

  // Compute unread count from conversations
  const computeUnreadCount = () => {
    unreadCount.value = conversations.value.reduce((count, conv) => {
      return count + (conv.unread_count || 0)
    }, 0)
  }

  // Fetch unread count (computed from conversations)
  const fetchUnreadCount = async (): Promise<void> => {
    try {
      await fetchConversations()
      computeUnreadCount()
    } catch (err) {
      // Silent fail for badge count
    }
  }

  // Clear current conversation
  const clearCurrentConversation = () => {
    currentConversation.value = []
    currentOtherUserId.value = null
  }

  return {
    // State
    conversations,
    currentConversation,
    currentOtherUserId,
    unreadCount,
    loading,
    error,
    // Getters
    hasUnreadMessages,
    sortedConversations,
    // Actions
    fetchConversations,
    fetchConversation,
    sendMessage,
    deleteMessage,
    fetchUnreadCount,
    clearCurrentConversation
  }
})

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex flex-col">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10 pointer-events-none">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <!-- Header -->
    <div class="relative bg-gray-800 bg-opacity-50 backdrop-blur-sm border-b border-white border-opacity-10">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center gap-4">
          <button @click="goBack" class="p-2 hover:bg-white hover:bg-opacity-10 rounded-lg transition-colors">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>

          <div class="flex items-center gap-3 flex-1">
            <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
              {{ otherUserInitials }}
            </div>
            <div>
              <h2 class="font-semibold text-white">{{ otherUserName }}</h2>
              <p v-if="apartmentContext" class="text-xs text-gray-400 truncate max-w-xs">
                Re: {{ apartmentContext.title }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages Container -->
    <div
      ref="messagesContainer"
      class="relative flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6"
    >
      <div class="max-w-4xl mx-auto space-y-4">
        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin w-8 h-8 border-2 border-secondary-500 border-t-transparent rounded-full"></div>
        </div>

        <!-- Messages -->
        <template v-else>
          <div
            v-for="message in messages"
            :key="message.id"
            :class="[
              'flex',
              message.sender_id === currentUserId ? 'justify-end' : 'justify-start'
            ]"
          >
            <div
              :class="[
                'max-w-[75%] px-4 py-3 rounded-2xl',
                message.sender_id === currentUserId
                  ? 'rounded-br-md text-white'
                  : 'bg-white bg-opacity-10 text-white rounded-bl-md'
              ]"
              :style="message.sender_id === currentUserId ? { background: 'linear-gradient(90deg, #4BC974 0%, #00A060 100%)' } : {}"
            >
              <p class="whitespace-pre-wrap break-words">{{ message.content }}</p>
              <div class="flex items-center justify-end gap-2 mt-1">
                <span class="text-xs opacity-70">{{ formatTime(message.created_at) }}</span>
                <svg
                  v-if="message.sender_id === currentUserId && message.is_read"
                  class="w-4 h-4 opacity-70"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
            </div>
          </div>
        </template>

        <!-- Empty State -->
        <div v-if="!loading && messages.length === 0" class="text-center py-12">
          <svg class="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          <p class="text-gray-400">{{ $t('common.noMessages') }}</p>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="relative bg-gray-800 bg-opacity-50 backdrop-blur-sm border-t border-white border-opacity-10">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <form @submit.prevent="sendMessage" class="flex items-end gap-3">
          <div class="flex-1">
            <textarea
              v-model="newMessage"
              @keydown.enter.exact.prevent="sendMessage"
              rows="1"
              :placeholder="$t('messages.typeMessage')"
              class="w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 resize-none max-h-32"
              :style="{ height: textareaHeight }"
              @input="adjustTextarea"
            ></textarea>
          </div>
          <button
            type="submit"
            :disabled="!newMessage.trim() || sending"
            class="p-3 rounded-xl text-white disabled:opacity-50 transition-all hover:shadow-lg disabled:hover:shadow-none"
            style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);"
          >
            <svg v-if="sending" class="w-6 h-6 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useMessageStore } from '@/stores/message'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()

const route = useRoute()
const router = useRouter()
const messageStore = useMessageStore()
const authStore = useAuthStore()

const messagesContainer = ref<HTMLElement | null>(null)
const newMessage = ref('')
const sending = ref(false)
const textareaHeight = ref('44px')

const messages = computed(() => messageStore.currentConversation)
const loading = computed(() => messageStore.loading)
const currentUserId = computed(() => authStore.user?.id)

const otherUserName = computed(() => {
  const conv = messageStore.conversations.find(
    (c) => c.other_user.id === Number(route.params.userId)
  )
  if (conv) {
    return `${conv.other_user.first_name} ${conv.other_user.last_name}`
  }
  return t('common.user')
})

const otherUserInitials = computed(() => {
  const conv = messageStore.conversations.find(
    (c) => c.other_user.id === Number(route.params.userId)
  )
  if (conv) {
    return `${conv.other_user.first_name?.charAt(0) || ''}${conv.other_user.last_name?.charAt(0) || ''}`.toUpperCase()
  }
  return 'U'
})

const apartmentContext = computed(() => {
  const conv = messageStore.conversations.find(
    (c) => c.other_user.id === Number(route.params.userId)
  )
  return conv?.apartment || null
})

const formatTime = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

const adjustTextarea = (e: Event) => {
  const target = e.target as HTMLTextAreaElement
  target.style.height = '44px'
  target.style.height = Math.min(target.scrollHeight, 128) + 'px'
  textareaHeight.value = target.style.height
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const goBack = () => {
  router.push({ name: 'messages' })
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || sending.value) return

  sending.value = true
  const content = newMessage.value
  newMessage.value = ''
  textareaHeight.value = '44px'

  const result = await messageStore.sendMessage({
    receiver_id: Number(route.params.userId),
    content,
    apartment_id: apartmentContext.value?.id
  })

  if (result) {
    scrollToBottom()
  }

  sending.value = false
}

const markMessagesAsRead = async () => {
  const unreadMessages = messages.value.filter(
    (m) => !m.is_read && m.sender_id !== currentUserId.value
  )
  if (unreadMessages.length > 0) {
    await messageStore.markAsRead(unreadMessages.map((m) => m.id))
  }
}

onMounted(async () => {
  const userId = Number(route.params.userId)
  if (userId) {
    await messageStore.fetchConversation(userId)
    scrollToBottom()
    markMessagesAsRead()
  }
})

watch(messages, () => {
  scrollToBottom()
  markMessagesAsRead()
})
</script>

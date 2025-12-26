<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Background pattern overlay -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-heading-1 text-white mb-2">{{ $t('messages.title') }}</h1>
        <p class="text-body text-gray-400">{{ $t('common.conversationsWith') }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="bg-white bg-opacity-5 rounded-xl p-4 animate-pulse">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gray-700 rounded-full"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-700 rounded w-1/3"></div>
              <div class="h-3 bg-gray-700 rounded w-2/3"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="conversations.length === 0" class="text-center py-16">
        <svg class="w-20 h-20 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
        <h3 class="text-heading-3 text-white mb-2">{{ $t('common.noMessagesYet') }}</h3>
        <p class="text-body text-gray-400 mb-6">{{ $t('common.startConversation') }}</p>
      </div>

      <!-- Conversations List -->
      <div v-else class="space-y-3">
        <router-link
          v-for="conversation in conversations"
          :key="conversation.other_user.id"
          :to="`/messages/${conversation.other_user.id}`"
          class="block bg-white bg-opacity-5 backdrop-blur-sm rounded-xl p-4 border border-white border-opacity-10 hover:bg-opacity-10 transition-all"
        >
          <div class="flex items-center gap-4">
            <!-- Avatar -->
            <div class="relative flex-shrink-0">
              <div class="w-12 h-12 rounded-full flex items-center justify-center text-white font-semibold text-lg" style="background: linear-gradient(90deg, #4BC974 0%, #00A060 100%);">
                {{ getInitials(conversation.other_user) }}
              </div>
              <div
                v-if="conversation.unread_count > 0"
                class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-xs font-bold text-white"
              >
                {{ conversation.unread_count > 9 ? '9+' : conversation.unread_count }}
              </div>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-1">
                <h3 class="font-semibold text-white truncate">
                  {{ conversation.other_user.first_name }} {{ conversation.other_user.last_name }}
                </h3>
                <span class="text-xs text-gray-400 flex-shrink-0 ml-2">
                  {{ formatTime(conversation.last_message.created_at) }}
                </span>
              </div>
              <p :class="[
                'text-sm truncate',
                conversation.unread_count > 0 ? 'text-white font-medium' : 'text-gray-400'
              ]">
                {{ conversation.last_message.content }}
              </p>
              <p v-if="conversation.apartment" class="text-xs text-secondary-400 mt-1 truncate">
                Re: {{ conversation.apartment.title }}
              </p>
            </div>

            <!-- Arrow -->
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useMessageStore } from '@/stores/message'
import type { User } from '@/types'
import BaseButton from '@/components/buttons/BaseButton.vue'

const { t } = useI18n()

const messageStore = useMessageStore()

const conversations = computed(() => messageStore.sortedConversations)
const loading = computed(() => messageStore.loading)

const getInitials = (user: User) => {
  return `${user.first_name?.charAt(0) || ''}${user.last_name?.charAt(0) || ''}`.toUpperCase()
}

const formatTime = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return t('common.justNow')
  if (diffMins < 60) return `${diffMins}${t('common.m')} ${t('common.ago')}`
  if (diffHours < 24) return `${diffHours}${t('common.h')} ${t('common.ago')}`
  if (diffDays < 7) return `${diffDays}${t('common.d')} ${t('common.ago')}`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

onMounted(() => {
  messageStore.fetchConversations()
})
</script>

import { apiClient } from './client'
import type { ConversationListItem, Conversation, ConversationStatusResponse } from '@/types/conversation'
import type { Message } from '@/types/message'

export const conversationsApi = {
  list: async (): Promise<ConversationListItem[]> => {
    const { data } = await apiClient.get('/api/conversations')
    return data
  },

  get: async (id: string): Promise<Conversation> => {
    const { data } = await apiClient.get(`/api/conversations/${id}`)
    return data
  },

  getMessages: async (id: string): Promise<Message[]> => {
    const { data } = await apiClient.get(`/api/conversations/${id}/messages`)
    return data
  },

  getStatus: async (id: string): Promise<ConversationStatusResponse> => {
    const { data } = await apiClient.get(`/api/conversations/${id}/status`)
    return data
  },
}


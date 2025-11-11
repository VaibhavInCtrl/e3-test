import { useQuery } from '@tanstack/react-query'
import { conversationsApi } from '../api/conversations'

export const useConversations = () => {
  return useQuery({
    queryKey: ['conversations'],
    queryFn: conversationsApi.list,
  })
}

export const useConversation = (id: string) => {
  return useQuery({
    queryKey: ['conversations', id],
    queryFn: () => conversationsApi.get(id),
    enabled: !!id,
  })
}

export const useConversationMessages = (id: string) => {
  return useQuery({
    queryKey: ['conversations', id, 'messages'],
    queryFn: () => conversationsApi.getMessages(id),
    enabled: !!id,
  })
}


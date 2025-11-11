import { useQuery } from '@tanstack/react-query'
import { conversationsApi } from '../api/conversations'
import { ConversationStatus } from '@/types/conversation'

export const usePolling = (conversationId: string | null, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['conversations', conversationId, 'status'],
    queryFn: () => conversationsApi.getStatus(conversationId!),
    enabled: !!conversationId && enabled,
    refetchInterval: (query) => {
      const status = query.state.data?.status
      if (status === ConversationStatus.COMPLETED || status === ConversationStatus.FAILED) {
        return false
      }
      return 3000
    },
  })
}


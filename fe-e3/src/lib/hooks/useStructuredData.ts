import { useQuery } from '@tanstack/react-query'
import { conversationsApi } from '../api/conversations'

export const useStructuredData = (conversationId: string | null) => {
  return useQuery({
    queryKey: ['conversations', conversationId, 'structured-data'],
    queryFn: () => conversationsApi.getStructuredData(conversationId!),
    enabled: !!conversationId,
  })
}


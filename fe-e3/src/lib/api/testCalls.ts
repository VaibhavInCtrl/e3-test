import { apiClient } from './client'
import type { StartTestCallRequest } from '@/types/testCall'
import type { Conversation } from '@/types/conversation'

export const testCallsApi = {
  start: async (request: StartTestCallRequest): Promise<Conversation> => {
    const { data } = await apiClient.post('/api/test-calls/start', request)
    return data
  },
}


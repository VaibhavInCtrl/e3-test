import { useMutation, useQueryClient } from '@tanstack/react-query'
import { testCallsApi } from '../api/testCalls'
import type { StartTestCallRequest } from '@/types/testCall'

export const useStartTestCall = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (request: StartTestCallRequest) => testCallsApi.start(request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
      queryClient.invalidateQueries({ queryKey: ['agents'] })
    },
  })
}


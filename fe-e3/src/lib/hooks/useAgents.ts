import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { agentsApi } from '../api/agents'
import type { AgentCreate, AgentUpdate } from '@/types/agent'

export const useAgents = () => {
  return useQuery({
    queryKey: ['agents'],
    queryFn: agentsApi.list,
  })
}

export const useAgent = (id: string) => {
  return useQuery({
    queryKey: ['agents', id],
    queryFn: () => agentsApi.get(id),
    enabled: !!id,
  })
}

export const useCreateAgent = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (agent: AgentCreate) => agentsApi.create(agent),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] })
    },
  })
}

export const useUpdateAgent = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: AgentUpdate }) =>
      agentsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] })
    },
  })
}

export const useDeleteAgent = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => agentsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] })
    },
  })
}


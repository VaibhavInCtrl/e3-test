import { apiClient } from './client'
import type { Agent, AgentListItem, AgentCreate, AgentUpdate, GeneratePromptRequest, GeneratePromptResponse } from '@/types/agent'

export const agentsApi = {
  list: async (): Promise<AgentListItem[]> => {
    const { data } = await apiClient.get('/api/agents')
    return data
  },

  get: async (id: string): Promise<Agent> => {
    const { data } = await apiClient.get(`/api/agents/${id}`)
    return data
  },

  create: async (agent: AgentCreate): Promise<Agent> => {
    const { data } = await apiClient.post('/api/agents', agent)
    return data
  },

  update: async (id: string, agent: AgentUpdate): Promise<Agent> => {
    const { data } = await apiClient.put(`/api/agents/${id}`, agent)
    return data
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/agents/${id}`)
  },

  generatePrompt: async (request: GeneratePromptRequest): Promise<GeneratePromptResponse> => {
    const { data } = await apiClient.post('/api/agents/generate-prompt', request)
    return data
  },
}

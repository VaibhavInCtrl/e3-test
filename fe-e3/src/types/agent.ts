export interface Agent {
  id: string
  name: string
  prompts: string
  additional_details: string | null
  created_at: string
  last_used_at: string | null
}

export interface AgentListItem {
  id: string
  name: string
  created_at: string
  last_used_at: string | null
  conversation_count: number
}

export interface AgentCreate {
  name: string
  prompts: string
  additional_details?: string
}

export interface AgentUpdate {
  name?: string
  prompts?: string
  additional_details?: string
}


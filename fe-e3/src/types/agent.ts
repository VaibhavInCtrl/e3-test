export interface Agent {
  id: string
  name: string
  prompts: string
  additional_details: string | null
  scenario_description: string | null
  system_prompt: string | null
  retell_agent_id: string | null
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
  scenario_description?: string
}

export interface AgentUpdate {
  name?: string
  prompts?: string
  additional_details?: string
  scenario_description?: string
}

export interface GeneratePromptRequest {
  scenario_description: string
  additional_context?: string
}

export interface GeneratePromptResponse {
  system_prompt: string
}

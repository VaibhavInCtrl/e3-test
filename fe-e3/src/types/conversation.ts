export enum ConversationStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface Conversation {
  id: string
  agent_id: string
  driver_id: string
  load_number: string
  status: ConversationStatus
  started_at: string
  completed_at: string | null
  retell_call_id: string | null
  retell_access_token: string | null
  recording_url: string | null
  transcript: string | null
  duration_ms: number | null
  structured_data: Record<string, any> | null
}

export interface ConversationListItem {
  id: string
  agent_id: string
  agent_name: string
  driver_id: string
  driver_name: string
  load_number: string
  status: ConversationStatus
  started_at: string
  completed_at: string | null
}

export interface ConversationStatusResponse {
  id: string
  status: ConversationStatus
  completed_at: string | null
}

export interface StructuredDataResponse {
  conversation_id: string
  structured_data: Record<string, any> | null
  recording_url: string | null
  duration_ms: number | null
}

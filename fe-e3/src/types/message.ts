export enum MessageRole {
  AGENT = 'agent',
  HUMAN = 'human'
}

export interface Message {
  id: string
  conversation_id: string
  role: MessageRole
  content: string
  created_at: string
}


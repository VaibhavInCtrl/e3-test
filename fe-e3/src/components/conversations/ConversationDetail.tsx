import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { MessageBubble } from './MessageBubble'
import { useConversation, useConversationMessages } from '@/lib/hooks/useConversations'
import { ConversationStatus } from '@/types/conversation'
import { formatDate } from '@/lib/utils'

interface ConversationDetailProps {
  conversationId: string
  onClose: () => void
}

const statusColors = {
  [ConversationStatus.PENDING]: 'bg-yellow-500',
  [ConversationStatus.IN_PROGRESS]: 'bg-blue-500',
  [ConversationStatus.COMPLETED]: 'bg-green-500',
  [ConversationStatus.FAILED]: 'bg-red-500',
}

export function ConversationDetail({ conversationId, onClose }: ConversationDetailProps) {
  const { data: conversation, isLoading: conversationLoading } = useConversation(conversationId)
  const { data: messages = [], isLoading: messagesLoading } = useConversationMessages(conversationId)

  if (conversationLoading || messagesLoading) {
    return (
      <Card className="h-full">
        <CardContent className="flex items-center justify-center h-full">
          <p className="text-muted-foreground">Loading conversation...</p>
        </CardContent>
      </Card>
    )
  }

  if (!conversation) {
    return null
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={onClose}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <CardTitle>Conversation Details</CardTitle>
        </div>
      </CardHeader>
      <Separator />
      <CardContent className="flex-1 overflow-auto p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Load Number</p>
            <p className="font-medium">{conversation.load_number}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Status</p>
            <Badge className={statusColors[conversation.status]}>
              {conversation.status.replace('_', ' ')}
            </Badge>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Started</p>
            <p className="font-medium">{formatDate(conversation.started_at)}</p>
          </div>
          {conversation.completed_at && (
            <div>
              <p className="text-sm text-muted-foreground">Completed</p>
              <p className="font-medium">{formatDate(conversation.completed_at)}</p>
            </div>
          )}
        </div>

        <Separator />

        <div>
          <h3 className="font-semibold mb-4">Transcript</h3>
          {messages.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">
              No messages yet
            </p>
          ) : (
            <div className="space-y-2">
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}


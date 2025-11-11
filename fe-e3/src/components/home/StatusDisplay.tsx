import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { ExternalLink, Loader2 } from 'lucide-react'
import { ConversationStatus, type Conversation } from '@/types/conversation'
import { usePolling } from '@/lib/hooks/usePolling'
import { useConversationMessages } from '@/lib/hooks/useConversations'
import { MessageBubble } from '@/components/conversations/MessageBubble'
import { formatDate } from '@/lib/utils'

interface StatusDisplayProps {
  conversation: Conversation
}

const statusColors = {
  [ConversationStatus.PENDING]: 'bg-yellow-500',
  [ConversationStatus.IN_PROGRESS]: 'bg-blue-500',
  [ConversationStatus.COMPLETED]: 'bg-green-500',
  [ConversationStatus.FAILED]: 'bg-red-500',
}

export function StatusDisplay({ conversation }: StatusDisplayProps) {
  const { data: statusData } = usePolling(conversation.id, true)
  const { data: messages = [] } = useConversationMessages(conversation.id)

  const currentStatus = statusData?.status || conversation.status
  const isInProgress = currentStatus === ConversationStatus.IN_PROGRESS || currentStatus === ConversationStatus.PENDING

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Call Status</CardTitle>
          <Link to="/conversations">
            <Button variant="outline" size="sm">
              <ExternalLink className="mr-2 h-4 w-4" />
              View All Conversations
            </Button>
          </Link>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Load Number</p>
            <p className="font-medium">{conversation.load_number}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Status</p>
            <div className="flex items-center gap-2">
              <Badge className={statusColors[currentStatus]}>
                {currentStatus.replace('_', ' ')}
              </Badge>
              {isInProgress && <Loader2 className="h-4 w-4 animate-spin" />}
            </div>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Started</p>
            <p className="font-medium">{formatDate(conversation.started_at)}</p>
          </div>
          {statusData?.completed_at && (
            <div>
              <p className="text-sm text-muted-foreground">Completed</p>
              <p className="font-medium">{formatDate(statusData.completed_at)}</p>
            </div>
          )}
        </div>

        {messages.length > 0 && (
          <>
            <Separator />
            <div>
              <h3 className="font-semibold mb-4">Live Transcript</h3>
              <div className="space-y-2 max-h-[400px] overflow-y-auto">
                {messages.map((message) => (
                  <MessageBubble key={message.id} message={message} />
                ))}
              </div>
            </div>
          </>
        )}

        {currentStatus === ConversationStatus.COMPLETED && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-sm font-medium text-green-900">
              Call completed successfully!
            </p>
          </div>
        )}

        {currentStatus === ConversationStatus.FAILED && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm font-medium text-red-900">
              Call failed. Please try again.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}


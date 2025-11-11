import { cn } from '@/lib/utils'
import { MessageRole, type Message } from '@/types/message'
import { formatDate } from '@/lib/utils'

interface MessageBubbleProps {
  message: Message
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isAgent = message.role === MessageRole.AGENT

  return (
    <div className={cn('flex mb-4', isAgent ? 'justify-start' : 'justify-end')}>
      <div className={cn('max-w-[70%] rounded-lg px-4 py-2', isAgent ? 'bg-muted' : 'bg-primary text-primary-foreground')}>
        <div className="text-xs font-semibold mb-1">
          {isAgent ? 'Agent' : 'Driver'}
        </div>
        <div className="text-sm whitespace-pre-wrap">{message.content}</div>
        <div className={cn('text-xs mt-1', isAgent ? 'text-muted-foreground' : 'opacity-70')}>
          {formatDate(message.created_at)}
        </div>
      </div>
    </div>
  )
}


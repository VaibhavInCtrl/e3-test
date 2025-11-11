import { Badge } from '@/components/ui/badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { formatRelativeTime } from '@/lib/utils'
import { ConversationStatus, type ConversationListItem } from '@/types/conversation'

interface ConversationListProps {
  conversations: ConversationListItem[]
  onView: (id: string) => void
}

const statusColors = {
  [ConversationStatus.PENDING]: 'bg-yellow-500',
  [ConversationStatus.IN_PROGRESS]: 'bg-blue-500',
  [ConversationStatus.COMPLETED]: 'bg-green-500',
  [ConversationStatus.FAILED]: 'bg-red-500',
}

export function ConversationList({ conversations, onView }: ConversationListProps) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Agent</TableHead>
            <TableHead>Driver</TableHead>
            <TableHead>Load Number</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Started</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {conversations.length === 0 ? (
            <TableRow>
              <TableCell colSpan={5} className="text-center text-muted-foreground">
                No conversations found. Start a test call to create one.
              </TableCell>
            </TableRow>
          ) : (
            conversations.map((conversation) => (
              <TableRow 
                key={conversation.id}
                className="cursor-pointer hover:bg-muted/50"
                onClick={() => onView(conversation.id)}
              >
                <TableCell className="font-medium">{conversation.agent_name}</TableCell>
                <TableCell>{conversation.driver_name}</TableCell>
                <TableCell>{conversation.load_number}</TableCell>
                <TableCell>
                  <Badge className={statusColors[conversation.status]}>
                    {conversation.status.replace('_', ' ')}
                  </Badge>
                </TableCell>
                <TableCell>{formatRelativeTime(conversation.started_at)}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}


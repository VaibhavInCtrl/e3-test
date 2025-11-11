import { ArrowLeft, Pencil } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useAgent } from '@/lib/hooks/useAgents'
import { useConversations } from '@/lib/hooks/useConversations'
import { formatDate, formatRelativeTime } from '@/lib/utils'
import { ConversationStatus } from '@/types/conversation'
import { useMemo } from 'react'

interface AgentDetailProps {
  agentId: string
  onClose: () => void
  onEdit: () => void
  onViewConversation: (conversationId: string) => void
}

const statusColors = {
  [ConversationStatus.PENDING]: 'bg-yellow-500',
  [ConversationStatus.IN_PROGRESS]: 'bg-blue-500',
  [ConversationStatus.COMPLETED]: 'bg-green-500',
  [ConversationStatus.FAILED]: 'bg-red-500',
}

export function AgentDetail({ agentId, onClose, onEdit, onViewConversation }: AgentDetailProps) {
  const { data: agent, isLoading: agentLoading } = useAgent(agentId)
  const { data: allConversations = [], isLoading: conversationsLoading } = useConversations()

  const agentConversations = useMemo(() => {
    return allConversations.filter((conv) => conv.agent_id === agentId)
  }, [allConversations, agentId])

  if (agentLoading || conversationsLoading) {
    return (
      <Card className="h-full">
        <CardContent className="flex items-center justify-center h-full py-8">
          <p className="text-muted-foreground">Loading agent details...</p>
        </CardContent>
      </Card>
    )
  }

  if (!agent) {
    return null
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={onClose}>
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <CardTitle>Agent Details</CardTitle>
          </div>
          <Button variant="outline" onClick={onEdit}>
            <Pencil className="mr-2 h-4 w-4" />
            Edit Agent
          </Button>
        </CardHeader>
        <Separator />
        <CardContent className="pt-6 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Name</p>
              <p className="font-medium">{agent.name}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Created</p>
              <p className="font-medium">{formatDate(agent.created_at)}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Last Used</p>
              <p className="font-medium">
                {agent.last_used_at ? formatRelativeTime(agent.last_used_at) : 'Never'}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Conversations</p>
              <p className="font-medium">{agentConversations.length}</p>
            </div>
          </div>

          <Separator />

          <div>
            <p className="text-sm text-muted-foreground mb-2">Scenario Description</p>
            <div className="bg-muted p-4 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm">{agent.scenario_description || agent.prompts}</pre>
            </div>
          </div>

          {agent.system_prompt && (
            <div>
              <p className="text-sm text-muted-foreground mb-2">Generated System Prompt</p>
              <div className="bg-muted p-4 rounded-lg max-h-[300px] overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm">{agent.system_prompt}</pre>
              </div>
            </div>
          )}

          {agent.additional_details && (
            <div>
              <p className="text-sm text-muted-foreground mb-2">Additional Details</p>
              <div className="bg-muted p-4 rounded-lg">
                <pre className="whitespace-pre-wrap text-sm">{agent.additional_details}</pre>
              </div>
            </div>
          )}

          {agent.retell_agent_id && (
            <div>
              <p className="text-sm text-muted-foreground mb-2">Retell Agent ID</p>
              <p className="font-mono text-sm">{agent.retell_agent_id}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Conversations ({agentConversations.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {agentConversations.length === 0 ? (
            <p className="text-center py-8 text-muted-foreground">
              No conversations found for this agent
            </p>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Driver</TableHead>
                    <TableHead>Load Number</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Started</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {agentConversations.map((conversation) => (
                    <TableRow
                      key={conversation.id}
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() => onViewConversation(conversation.id)}
                    >
                      <TableCell className="font-medium">{conversation.driver_name}</TableCell>
                      <TableCell>{conversation.load_number}</TableCell>
                      <TableCell>
                        <Badge className={statusColors[conversation.status]}>
                          {conversation.status.replace('_', ' ')}
                        </Badge>
                      </TableCell>
                      <TableCell>{formatRelativeTime(conversation.started_at)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}


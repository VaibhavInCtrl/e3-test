import { MoreHorizontal, Pencil, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { formatRelativeTime } from '@/lib/utils'
import type { AgentListItem } from '@/types/agent'

interface AgentListProps {
  agents: AgentListItem[]
  onView: (agent: AgentListItem) => void
  onEdit: (agent: AgentListItem) => void
  onDelete: (id: string) => void
}

export function AgentList({ agents, onView, onEdit, onDelete }: AgentListProps) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Created</TableHead>
            <TableHead>Last Used</TableHead>
            <TableHead>Conversations</TableHead>
            <TableHead className="w-[70px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {agents.length === 0 ? (
            <TableRow>
              <TableCell colSpan={5} className="text-center text-muted-foreground">
                No agents found. Create your first agent to get started.
              </TableCell>
            </TableRow>
          ) : (
            agents.map((agent) => (
              <TableRow key={agent.id} className="cursor-pointer hover:bg-muted/50">
                <TableCell 
                  className="font-medium"
                  onClick={() => onView(agent)}
                >
                  {agent.name}
                </TableCell>
                <TableCell onClick={() => onView(agent)}>
                  {formatRelativeTime(agent.created_at)}
                </TableCell>
                <TableCell onClick={() => onView(agent)}>
                  {agent.last_used_at ? formatRelativeTime(agent.last_used_at) : 'Never'}
                </TableCell>
                <TableCell onClick={() => onView(agent)}>
                  {agent.conversation_count}
                </TableCell>
                <TableCell>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" onClick={(e) => e.stopPropagation()}>
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={(e) => {
                        e.stopPropagation()
                        onEdit(agent)
                      }}>
                        <Pencil className="mr-2 h-4 w-4" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem
                        onClick={(e) => {
                          e.stopPropagation()
                          onDelete(agent.id)
                        }}
                        className="text-destructive"
                      >
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}


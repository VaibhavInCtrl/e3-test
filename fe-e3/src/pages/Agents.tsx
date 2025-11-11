import { useState, useMemo } from 'react'
import { Plus } from 'lucide-react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { SearchInput } from '@/components/ui/search-input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { AgentList } from '@/components/agents/AgentList'
import { AgentForm } from '@/components/agents/AgentForm'
import { useAgents, useAgent, useCreateAgent, useUpdateAgent, useDeleteAgent } from '@/lib/hooks/useAgents'
import type { AgentListItem } from '@/types/agent'

export default function Agents() {
  const [formOpen, setFormOpen] = useState(false)
  const [editingAgentId, setEditingAgentId] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<string>('created_desc')

  const { data: agents = [], isLoading } = useAgents()
  const { data: editingAgent } = useAgent(editingAgentId || '')
  const createAgent = useCreateAgent()
  const updateAgent = useUpdateAgent()
  const deleteAgent = useDeleteAgent()

  const filteredAndSortedAgents = useMemo(() => {
    let filtered = agents.filter((agent) =>
      agent.name.toLowerCase().includes(searchQuery.toLowerCase())
    )

    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'created_desc':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        case 'created_asc':
          return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        case 'last_used_desc':
          if (!a.last_used_at) return 1
          if (!b.last_used_at) return -1
          return new Date(b.last_used_at).getTime() - new Date(a.last_used_at).getTime()
        case 'last_used_asc':
          if (!a.last_used_at) return 1
          if (!b.last_used_at) return -1
          return new Date(a.last_used_at).getTime() - new Date(b.last_used_at).getTime()
        case 'conversations_desc':
          return b.conversation_count - a.conversation_count
        case 'conversations_asc':
          return a.conversation_count - b.conversation_count
        default:
          return 0
      }
    })

    return filtered
  }, [agents, searchQuery, sortBy])

  const handleCreate = (data: any) => {
    createAgent.mutate(data, {
      onSuccess: () => {
        setFormOpen(false)
        toast.success('Agent created successfully')
      },
      onError: () => {
        toast.error('Failed to create agent')
      },
    })
  }

  const handleUpdate = (data: any) => {
    if (editingAgentId) {
      updateAgent.mutate(
        { id: editingAgentId, data },
        {
          onSuccess: () => {
            setEditingAgentId(null)
            setFormOpen(false)
            toast.success('Agent updated successfully')
          },
          onError: () => {
            toast.error('Failed to update agent')
          },
        }
      )
    }
  }

  const handleEdit = (agent: AgentListItem) => {
    setEditingAgentId(agent.id)
    setFormOpen(true)
  }

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this agent?')) {
      deleteAgent.mutate(id, {
        onSuccess: () => {
          toast.success('Agent deleted successfully')
        },
        onError: () => {
          toast.error('Failed to delete agent')
        },
      })
    }
  }

  const handleOpenChange = (open: boolean) => {
    setFormOpen(open)
    if (!open) {
      setEditingAgentId(null)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Agents</h1>
          <p className="text-muted-foreground">
            Manage your AI agents and their configurations
          </p>
        </div>
        <Button onClick={() => setFormOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Agent
        </Button>
      </div>

      <div className="flex gap-4">
        <div className="flex-1">
          <SearchInput
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search agents by name..."
          />
        </div>
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="created_desc">Newest First</SelectItem>
            <SelectItem value="created_asc">Oldest First</SelectItem>
            <SelectItem value="last_used_desc">Recently Used</SelectItem>
            <SelectItem value="last_used_asc">Least Used</SelectItem>
            <SelectItem value="conversations_desc">Most Conversations</SelectItem>
            <SelectItem value="conversations_asc">Least Conversations</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {isLoading ? (
        <div className="text-center py-8 text-muted-foreground">Loading agents...</div>
      ) : (
        <AgentList agents={filteredAndSortedAgents} onEdit={handleEdit} onDelete={handleDelete} />
      )}

      <AgentForm
        open={formOpen}
        onOpenChange={handleOpenChange}
        onSubmit={editingAgentId ? handleUpdate : handleCreate}
        agent={editingAgent}
        isLoading={createAgent.isPending || updateAgent.isPending}
      />
    </div>
  )
}


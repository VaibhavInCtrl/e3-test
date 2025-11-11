import { useState, useMemo } from 'react'
import { SearchInput } from '@/components/ui/search-input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { ConversationList } from '@/components/conversations/ConversationList'
import { ConversationDetail } from '@/components/conversations/ConversationDetail'
import { useConversations } from '@/lib/hooks/useConversations'
import { ConversationStatus } from '@/types/conversation'

export default function Conversations() {
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [sortBy, setSortBy] = useState<string>('created_desc')

  const { data: conversations = [], isLoading } = useConversations()

  const filteredAndSortedConversations = useMemo(() => {
    let filtered = conversations.filter((conv) => {
      const matchesSearch =
        conv.agent_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        conv.driver_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        conv.load_number.toLowerCase().includes(searchQuery.toLowerCase())

      const matchesStatus = statusFilter === 'all' || conv.status === statusFilter

      return matchesSearch && matchesStatus
    })

    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'created_desc':
          return new Date(b.started_at).getTime() - new Date(a.started_at).getTime()
        case 'created_asc':
          return new Date(a.started_at).getTime() - new Date(b.started_at).getTime()
        default:
          return 0
      }
    })

    return filtered
  }, [conversations, searchQuery, statusFilter, sortBy])

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Conversations</h1>
        <p className="text-muted-foreground">
          View all conversations and their transcripts
        </p>
      </div>

      {selectedConversationId ? (
        <ConversationDetail
          conversationId={selectedConversationId}
          onClose={() => setSelectedConversationId(null)}
        />
      ) : (
        <>
          <div className="flex gap-4">
            <div className="flex-1">
              <SearchInput
                value={searchQuery}
                onChange={setSearchQuery}
                placeholder="Search by agent, driver, or load number..."
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value={ConversationStatus.PENDING}>Pending</SelectItem>
                <SelectItem value={ConversationStatus.IN_PROGRESS}>In Progress</SelectItem>
                <SelectItem value={ConversationStatus.COMPLETED}>Completed</SelectItem>
                <SelectItem value={ConversationStatus.FAILED}>Failed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="created_desc">Newest First</SelectItem>
                <SelectItem value="created_asc">Oldest First</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Loading conversations...</div>
          ) : (
            <ConversationList
              conversations={filteredAndSortedConversations}
              onView={setSelectedConversationId}
            />
          )}
        </>
      )}
    </div>
  )
}


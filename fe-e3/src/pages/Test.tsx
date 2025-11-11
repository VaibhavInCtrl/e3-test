import { useState } from 'react'
import { toast } from 'sonner'
import { TestCallForm } from '@/components/home/TestCallForm'
import { StatusDisplay } from '@/components/home/StatusDisplay'
import { useStartTestCall } from '@/lib/hooks/useTestCall'
import type { Conversation } from '@/types/conversation'

export default function Test() {
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null)
  const startTestCall = useStartTestCall()

  const handleStartCall = (data: any) => {
    startTestCall.mutate(data, {
      onSuccess: (conversation) => {
        setCurrentConversation(conversation)
        toast.success('Test call started successfully')
      },
      onError: () => {
        toast.error('Failed to start test call')
      },
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Test</h1>
        <p className="text-muted-foreground">
          Start a new test call with an agent and driver
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <TestCallForm
          onSubmit={handleStartCall}
          isLoading={startTestCall.isPending}
        />
        {currentConversation && (
          <StatusDisplay conversation={currentConversation} />
        )}
      </div>
    </div>
  )
}


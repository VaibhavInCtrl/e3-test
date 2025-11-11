import { useState } from 'react'
import { toast } from 'sonner'
import { TestCallForm } from '@/components/home/TestCallForm'
import { StatusDisplay } from '@/components/home/StatusDisplay'
import { WebCallInterface } from '@/components/home/WebCallInterface'
import { useStartTestCall } from '@/lib/hooks/useTestCall'
import type { Conversation } from '@/types/conversation'

export default function Test() {
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null)
  const [showWebCall, setShowWebCall] = useState(false)
  const startTestCall = useStartTestCall()

  const handleStartCall = (data: any) => {
    startTestCall.mutate(data, {
      onSuccess: (conversation) => {
        setCurrentConversation(conversation)
        setShowWebCall(true)
        toast.success('Test call started successfully')
      },
      onError: () => {
        toast.error('Failed to start test call')
      },
    })
  }

  const handleCallEnd = () => {
    setShowWebCall(false)
    toast.info('Call ended')
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
        {!showWebCall ? (
          <TestCallForm
            onSubmit={handleStartCall}
            isLoading={startTestCall.isPending}
          />
        ) : (
          currentConversation?.retell_access_token && (
            <WebCallInterface
              accessToken={currentConversation.retell_access_token}
              conversationId={currentConversation.id}
              onCallEnd={handleCallEnd}
            />
          )
        )}
        {currentConversation && (
          <StatusDisplay conversation={currentConversation} />
        )}
      </div>
    </div>
  )
}


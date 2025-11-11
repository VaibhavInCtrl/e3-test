import { useEffect, useRef, useState } from 'react'
import { RetellWebClient } from 'retell-client-js-sdk'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Mic, Phone, PhoneOff } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { testCallsApi } from '@/lib/api/testCalls'

interface WebCallInterfaceProps {
  accessToken: string
  conversationId: string
  onCallEnd: () => void
}

export function WebCallInterface({ accessToken, conversationId, onCallEnd }: WebCallInterfaceProps) {
  const retellClient = useRef<RetellWebClient | null>(null)
  const [isCallActive, setIsCallActive] = useState(false)
  const [isAgentSpeaking, setIsAgentSpeaking] = useState(false)
  const [transcript, setTranscript] = useState<string>('')
  const [error, setError] = useState<string | null>(null)
  const [connectionStatus, setConnectionStatus] = useState<string>('Initializing...')

  useEffect(() => {
    let mounted = true
    
    const initCall = async () => {
      if (!mounted) return
      
      try {
        setConnectionStatus('Requesting microphone access...')
        
        await navigator.mediaDevices.getUserMedia({ audio: true })
        
        if (!mounted) return
        
        setConnectionStatus('Initializing call...')
        retellClient.current = new RetellWebClient()

        retellClient.current.on('call_started', () => {
          if (!mounted) return
          setIsCallActive(true)
          setError(null)
          setConnectionStatus('Connected - Speak now!')
        })

        retellClient.current.on('call_ended', () => {
          if (!mounted) return
          setIsCallActive(false)
          setConnectionStatus('Call ended')
          setTimeout(() => {
            if (mounted) onCallEnd()
          }, 1000)
        })

        retellClient.current.on('agent_start_talking', () => {
          if (!mounted) return
          setIsAgentSpeaking(true)
        })

        retellClient.current.on('agent_stop_talking', () => {
          if (!mounted) return
          setIsAgentSpeaking(false)
        })

        retellClient.current.on('update', (update) => {
          if (!mounted) return
          if (update.transcript) {
            const transcriptText = typeof update.transcript === 'string' 
              ? update.transcript 
              : JSON.stringify(update.transcript, null, 2)
            setTranscript(transcriptText)
          }
        })

        retellClient.current.on('error', (error) => {
          console.error('Retell error:', error)
          if (!mounted) return
          setError(`Connection error: ${error.message || 'Unknown error'}. Please try again.`)
          setIsCallActive(false)
          setConnectionStatus('Error')
        })

        retellClient.current.on('disconnect', (reason) => {
          console.log('Disconnected:', reason)
        })

        if (!mounted) return
        
        setConnectionStatus('Connecting to agent...')
        
        await retellClient.current.startCall({
          accessToken: accessToken,
          sampleRate: 24000,
          emitRawAudioSamples: false
        })
      } catch (err: any) {
        console.error('Failed to start call:', err)
        if (!mounted) return
        
        if (err.name === 'NotAllowedError') {
          setError('Microphone access denied. Please allow microphone access and try again.')
        } else {
          setError(err.message || 'Failed to start call')
        }
        setIsCallActive(false)
        setConnectionStatus('Failed')
      }
    }

    initCall()

    return () => {
      mounted = false
      if (retellClient.current) {
        try {
          retellClient.current.stopCall()
        } catch (e) {
          console.error('Error stopping call:', e)
        }
      }
    }
  }, [accessToken, onCallEnd])

  const handleEndCall = async () => {
    if (retellClient.current) {
      retellClient.current.stopCall()
    }
    
    try {
      await testCallsApi.endCall(conversationId)
      setConnectionStatus('Processing...')
    } catch (err) {
      console.error('Failed to end call:', err)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Phone className="h-5 w-5" />
          Live Call
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm font-medium text-red-900">{error}</p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-center gap-4">
              <Badge variant={isCallActive ? 'default' : 'secondary'} className="text-lg px-4 py-2">
                {connectionStatus}
              </Badge>
              {isAgentSpeaking && (
                <Badge variant="outline" className="animate-pulse">
                  <Mic className="h-3 w-3 mr-1" />
                  Agent Speaking
                </Badge>
              )}
            </div>

            <div className="text-center space-y-2">
              <div className="flex items-center justify-center">
                <div className={`w-16 h-16 rounded-full flex items-center justify-center ${isAgentSpeaking ? 'bg-primary animate-pulse' : 'bg-muted'}`}>
                  <Mic className="h-8 w-8 text-primary-foreground" />
                </div>
              </div>
              <p className="text-sm text-muted-foreground">
                {isCallActive ? 'Speak now - the agent is listening' : 'Establishing connection...'}
              </p>
            </div>

            {transcript && (
              <div className="bg-muted p-4 rounded-lg max-h-[200px] overflow-y-auto">
                <p className="text-xs text-muted-foreground mb-2">Live Transcript:</p>
                <p className="text-sm whitespace-pre-wrap">{transcript}</p>
              </div>
            )}

            <Button
              variant="destructive"
              className="w-full"
              onClick={handleEndCall}
              disabled={!isCallActive}
            >
              <PhoneOff className="mr-2 h-4 w-4" />
              End Call
            </Button>
          </>
        )}
      </CardContent>
    </Card>
  )
}


import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { useAgents } from '@/lib/hooks/useAgents'
import { useDrivers } from '@/lib/hooks/useDrivers'
import { AgentForm } from '@/components/agents/AgentForm'
import { useCreateAgent } from '@/lib/hooks/useAgents'

const testCallSchema = z.object({
  agent_id: z.string().min(1, 'Agent is required'),
  driver_mode: z.enum(['existing', 'new']),
  driver_id: z.string().optional(),
  driver_name: z.string().optional(),
  driver_phone: z
    .string()
    .optional()
    .refine(
      (val) => !val || /^\+?\d+$/.test(val),
      'Phone number must contain only digits, optionally starting with +'
    ),
  load_number: z.string().min(1, 'Load number is required'),
}).refine((data) => {
  if (data.driver_mode === 'existing') {
    return !!data.driver_id
  } else {
    return !!data.driver_name && !!data.driver_phone
  }
}, {
  message: 'Driver information is required',
  path: ['driver_id'],
})

type TestCallFormData = z.infer<typeof testCallSchema>

interface TestCallFormProps {
  onSubmit: (data: any) => void
  isLoading?: boolean
}

export function TestCallForm({ onSubmit, isLoading }: TestCallFormProps) {
  const [driverMode, setDriverMode] = useState<'existing' | 'new'>('existing')
  const [agentFormOpen, setAgentFormOpen] = useState(false)

  const { data: agents = [] } = useAgents()
  const { data: drivers = [] } = useDrivers()
  const createAgent = useCreateAgent()

  const form = useForm<TestCallFormData>({
    resolver: zodResolver(testCallSchema),
    defaultValues: {
      agent_id: '',
      driver_mode: 'existing',
      driver_id: '',
      driver_name: '',
      driver_phone: '',
      load_number: '',
    },
  })

  const handleSubmit = (data: TestCallFormData) => {
    const payload: any = {
      agent_id: data.agent_id,
      load_number: data.load_number,
    }

    if (data.driver_mode === 'existing') {
      payload.driver_id = data.driver_id
    } else {
      payload.driver_name = data.driver_name
      payload.driver_phone = data.driver_phone
    }

    onSubmit(payload)
  }

  const handleCreateAgent = (data: any) => {
    createAgent.mutate(data, {
      onSuccess: (newAgent) => {
        setAgentFormOpen(false)
        form.setValue('agent_id', newAgent.id)
      },
    })
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Start Test Call</CardTitle>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
              <div className="flex items-end gap-2">
                <FormField
                  control={form.control}
                  name="agent_id"
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <FormLabel>Agent</FormLabel>
                      <Select onValueChange={field.onChange} value={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select an agent" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {agents.map((agent) => (
                            <SelectItem key={agent.id} value={agent.id}>
                              {agent.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setAgentFormOpen(true)}
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>

              <Separator />

              <div>
                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  Driver
                </label>
                <div className="flex gap-2 mt-2">
                  <Button
                    type="button"
                    variant={driverMode === 'existing' ? 'default' : 'outline'}
                    onClick={() => {
                      setDriverMode('existing')
                      form.setValue('driver_mode', 'existing')
                    }}
                    className="flex-1"
                  >
                    Existing Driver
                  </Button>
                  <Button
                    type="button"
                    variant={driverMode === 'new' ? 'default' : 'outline'}
                    onClick={() => {
                      setDriverMode('new')
                      form.setValue('driver_mode', 'new')
                    }}
                    className="flex-1"
                  >
                    New Driver
                  </Button>
                </div>
              </div>

              {driverMode === 'existing' ? (
                <FormField
                  control={form.control}
                  name="driver_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Select Driver</FormLabel>
                      <Select onValueChange={field.onChange} value={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Choose a driver" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {drivers.map((driver) => (
                            <SelectItem key={driver.id} value={driver.id}>
                              {driver.name} ({driver.phone_number})
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              ) : (
                <>
                  <FormField
                    control={form.control}
                    name="driver_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Driver Name</FormLabel>
                        <FormControl>
                          <Input placeholder="Enter driver name" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="driver_phone"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Driver Phone</FormLabel>
                        <FormControl>
                          <Input placeholder="+1234567890" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </>
              )}

              <FormField
                control={form.control}
                name="load_number"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Load Number</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter load number" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? 'Starting Call...' : 'Start Test Call'}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>

      <AgentForm
        open={agentFormOpen}
        onOpenChange={setAgentFormOpen}
        onSubmit={handleCreateAgent}
        isLoading={createAgent.isPending}
      />
    </>
  )
}


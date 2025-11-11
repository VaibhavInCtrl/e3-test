import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import type { Agent } from '@/types/agent'

const agentSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  prompts: z.string().min(1, 'Scenario description is required'),
  additional_details: z.string().optional(),
})

type AgentFormData = z.infer<typeof agentSchema>

interface AgentFormDataWithScenario extends AgentFormData {
  scenario_description?: string
}

interface AgentFormProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: AgentFormData) => void
  agent?: Agent
  isLoading?: boolean
}

export function AgentForm({ open, onOpenChange, onSubmit, agent, isLoading }: AgentFormProps) {
  const form = useForm<AgentFormData>({
    resolver: zodResolver(agentSchema),
    defaultValues: {
      name: '',
      prompts: '',
      additional_details: '',
    },
  })

  useEffect(() => {
    if (agent) {
      form.reset({
        name: agent.name,
        prompts: agent.prompts,
        additional_details: agent.additional_details || '',
      })
    } else {
      form.reset({
        name: '',
        prompts: '',
        additional_details: '',
      })
    }
  }, [agent, form])

  const handleSubmit = (data: AgentFormData) => {
    const submitData: AgentFormDataWithScenario = {
      ...data,
      scenario_description: data.prompts
    }
    onSubmit(submitData)
    form.reset()
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>{agent ? 'Edit Agent' : 'Create Agent'}</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="Agent name" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="prompts"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Scenario Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Describe what this agent should do and what data to extract...&#10;&#10;Example: Handle driver check-ins for load deliveries. Determine if driver is in-transit or arrived. For in-transit: get location, ETA, any delays. For arrived: get unloading status. Handle emergencies immediately. Extract: call_outcome, driver_status, current_location, eta, delay_reason, emergency_type."
                      className="min-h-[180px]"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="additional_details"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Additional Details (Optional)</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Additional logic, flows, or specific details..."
                      className="min-h-[80px]"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? 'Saving...' : agent ? 'Update' : 'Create'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}


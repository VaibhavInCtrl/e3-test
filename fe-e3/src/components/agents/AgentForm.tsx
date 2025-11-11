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
  prompts: z.string().min(1, 'Prompts are required'),
  additional_details: z.string().optional(),
})

type AgentFormData = z.infer<typeof agentSchema>

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
    onSubmit(data)
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
                  <FormLabel>Prompts</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Enter agent prompts..."
                      className="min-h-[120px]"
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


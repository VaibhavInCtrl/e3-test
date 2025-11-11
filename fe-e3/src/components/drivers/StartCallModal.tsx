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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { useAgents } from '@/lib/hooks/useAgents'
import type { Driver } from '@/types/driver'

const startCallSchema = z.object({
  agent_id: z.string().min(1, 'Agent is required'),
  load_number: z.string().min(1, 'Load number is required'),
})

type StartCallFormData = z.infer<typeof startCallSchema>

interface StartCallModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: StartCallFormData) => void
  driver: Driver
  isLoading?: boolean
}

export function StartCallModal({ open, onOpenChange, onSubmit, driver, isLoading }: StartCallModalProps) {
  const { data: agents = [] } = useAgents()

  const form = useForm<StartCallFormData>({
    resolver: zodResolver(startCallSchema),
    defaultValues: {
      agent_id: '',
      load_number: '',
    },
  })

  const handleSubmit = (data: StartCallFormData) => {
    onSubmit(data)
    form.reset()
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Start Conversation with {driver.name}</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="agent_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Select Agent</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Choose an agent" />
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
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? 'Starting...' : 'Start Conversation'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}


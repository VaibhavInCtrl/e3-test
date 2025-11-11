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
import { DriverList } from '@/components/drivers/DriverList'
import { DriverForm } from '@/components/drivers/DriverForm'
import { useDrivers, useCreateDriver, useUpdateDriver, useDeleteDriver } from '@/lib/hooks/useDrivers'
import type { Driver } from '@/types/driver'

export default function Drivers() {
  const [formOpen, setFormOpen] = useState(false)
  const [editingDriver, setEditingDriver] = useState<Driver | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<string>('created_desc')

  const { data: drivers = [], isLoading } = useDrivers()
  const createDriver = useCreateDriver()
  const updateDriver = useUpdateDriver()
  const deleteDriver = useDeleteDriver()

  const filteredAndSortedDrivers = useMemo(() => {
    let filtered = drivers.filter((driver) =>
      driver.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      driver.phone_number.includes(searchQuery)
    )

    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'created_desc':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        case 'created_asc':
          return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        case 'name_asc':
          return a.name.localeCompare(b.name)
        case 'name_desc':
          return b.name.localeCompare(a.name)
        default:
          return 0
      }
    })

    return filtered
  }, [drivers, searchQuery, sortBy])

  const handleCreate = (data: any) => {
    createDriver.mutate(data, {
      onSuccess: () => {
        setFormOpen(false)
        toast.success('Driver created successfully')
      },
      onError: () => {
        toast.error('Failed to create driver')
      },
    })
  }

  const handleUpdate = (data: any) => {
    if (editingDriver) {
      updateDriver.mutate(
        { id: editingDriver.id, data },
        {
          onSuccess: () => {
            setEditingDriver(null)
            setFormOpen(false)
            toast.success('Driver updated successfully')
          },
          onError: () => {
            toast.error('Failed to update driver')
          },
        }
      )
    }
  }

  const handleEdit = (driver: Driver) => {
    setEditingDriver(driver)
    setFormOpen(true)
  }

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this driver?')) {
      deleteDriver.mutate(id, {
        onSuccess: () => {
          toast.success('Driver deleted successfully')
        },
        onError: () => {
          toast.error('Failed to delete driver')
        },
      })
    }
  }

  const handleFormOpenChange = (open: boolean) => {
    setFormOpen(open)
    if (!open) {
      setEditingDriver(null)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Drivers</h1>
          <p className="text-muted-foreground">
            Manage driver information
          </p>
        </div>
        <Button onClick={() => setFormOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Driver
        </Button>
      </div>

      <div className="flex gap-4">
        <div className="flex-1">
          <SearchInput
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search drivers by name or phone..."
          />
        </div>
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="created_desc">Newest First</SelectItem>
            <SelectItem value="created_asc">Oldest First</SelectItem>
            <SelectItem value="name_asc">Name (A-Z)</SelectItem>
            <SelectItem value="name_desc">Name (Z-A)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {isLoading ? (
        <div className="text-center py-8 text-muted-foreground">Loading drivers...</div>
      ) : (
        <DriverList
          drivers={filteredAndSortedDrivers}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}

      <DriverForm
        open={formOpen}
        onOpenChange={handleFormOpenChange}
        onSubmit={editingDriver ? handleUpdate : handleCreate}
        driver={editingDriver || undefined}
        isLoading={createDriver.isPending || updateDriver.isPending}
      />
    </div>
  )
}


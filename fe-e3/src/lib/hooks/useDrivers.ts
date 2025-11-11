import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { driversApi } from '../api/drivers'
import type { DriverCreate, DriverUpdate } from '@/types/driver'

export const useDrivers = () => {
  return useQuery({
    queryKey: ['drivers'],
    queryFn: driversApi.list,
  })
}

export const useDriver = (id: string) => {
  return useQuery({
    queryKey: ['drivers', id],
    queryFn: () => driversApi.get(id),
    enabled: !!id,
  })
}

export const useCreateDriver = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (driver: DriverCreate) => driversApi.create(driver),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drivers'] })
    },
  })
}

export const useUpdateDriver = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: DriverUpdate }) =>
      driversApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drivers'] })
    },
  })
}

export const useDeleteDriver = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => driversApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drivers'] })
    },
  })
}


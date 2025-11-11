import { apiClient } from './client'
import type { Driver, DriverCreate, DriverUpdate } from '@/types/driver'

export const driversApi = {
  list: async (): Promise<Driver[]> => {
    const { data } = await apiClient.get('/api/drivers')
    return data
  },

  get: async (id: string): Promise<Driver> => {
    const { data } = await apiClient.get(`/api/drivers/${id}`)
    return data
  },

  create: async (driver: DriverCreate): Promise<Driver> => {
    const { data } = await apiClient.post('/api/drivers', driver)
    return data
  },

  update: async (id: string, driver: DriverUpdate): Promise<Driver> => {
    const { data } = await apiClient.put(`/api/drivers/${id}`, driver)
    return data
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/drivers/${id}`)
  },
}


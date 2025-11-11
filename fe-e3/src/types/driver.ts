export interface Driver {
  id: string
  name: string
  phone_number: string
  created_at: string
}

export interface DriverCreate {
  name: string
  phone_number: string
}

export interface DriverUpdate {
  name?: string
  phone_number?: string
}


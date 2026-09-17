export interface ModbusRegister {
  address: number
  name: string
  type: 'coil' | 'discrete' | 'holding' | 'input'
  value: number | boolean
  unit: string
  updatedAt: number
}

export interface Device {
  id: string
  name: string
  ip: string
  port: number
  slaveId: number
  online: boolean
  registers: ModbusRegister[]
}

export interface Alarm {
  id: string
  deviceId: string
  register: string
  message: string
  level: 'info' | 'warning' | 'critical'
  timestamp: number
  acknowledged: boolean
}

// Shape of shared/devices.json — the single device/register definition
// shared with the backend (field names follow the backend API convention).
export interface RegisterDefinition {
  address: number
  name: string
  type: 'coil' | 'discrete' | 'holding' | 'input'
  value: number | boolean
  unit: string
}

export interface DeviceDefinition {
  id: string
  name: string
  ip: string
  port: number
  slave_id: number
  online: boolean
  registers: RegisterDefinition[]
}

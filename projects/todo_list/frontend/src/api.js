// API client - connected to the Hub's unified backend
const API_BASE_URL = '/api'

// --- TASKS ---
export const getTasks = async () => {
  const res = await fetch(`${API_BASE_URL}/tasks`)
  if (!res.ok) throw new Error(`Failed to fetch tasks: ${res.status}`)
  return res.json()
}

export const createTask = async (taskData) => {
  const res = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  })
  if (!res.ok) throw new Error(`Failed to create task: ${res.status}`)
  return res.json()
}

export const updateTask = async (taskId, updates) => {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  })
  if (!res.ok) throw new Error(`Failed to update task: ${res.status}`)
  return res.json()
}

export const deleteTask = async (taskId) => {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`Failed to delete task: ${res.status}`)
  return res.json()
}

// --- STEPS ---
export const createStep = async (taskId, stepData) => {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}/steps`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(stepData)
  })
  if (!res.ok) throw new Error(`Failed to create step: ${res.status}`)
  return res.json()
}

export const updateStep = async (stepId, isCompleted) => {
  const res = await fetch(`${API_BASE_URL}/tasks/steps/${stepId}?is_completed=${isCompleted}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' }
  })
  if (!res.ok) throw new Error(`Failed to update step: ${res.status}`)
  return res.json()
}

export const deleteStep = async (stepId) => {
  const res = await fetch(`${API_BASE_URL}/tasks/steps/${stepId}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`Failed to delete step: ${res.status}`)
  return res.json()
}

import type { SessionState } from './types'

const API_BASE = '/api'

export async function startSession(requirement: string): Promise<SessionState> {
  const response = await fetch(`${API_BASE}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ requirement }),
  })
  if (!response.ok) throw new Error('Failed to start session')
  return response.json()
}

export async function stepSession(sessionId: string, action: string): Promise<SessionState> {
  const response = await fetch(`${API_BASE}/step`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, action }),
  })
  if (!response.ok) throw new Error('Failed to step session')
  return response.json()
}

export async function resetSession(): Promise<void> {
  const response = await fetch(`${API_BASE}/reset`, { method: 'POST' })
  if (!response.ok) throw new Error('Failed to reset session')
}

export async function getSession(): Promise<SessionState | null> {
  const response = await fetch(`${API_BASE}/session`)
  if (response.status === 404) return null
  if (!response.ok) throw new Error('Failed to get session')
  return response.json()
}

export async function exportDocs(data: any): Promise<Blob> {
  const response = await fetch(`${API_BASE}/export/docs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!response.ok) throw new Error('Failed to export PDF')
  return response.blob()
}

export async function exportSlides(data: any): Promise<Blob> {
  const response = await fetch(`${API_BASE}/export/slides`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!response.ok) throw new Error('Failed to export PPTX')
  return response.blob()
}

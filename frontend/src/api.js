const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function buildHeaders(token, extra = {}) {
  return {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...extra
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options)
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.message || errorBody.detail || `Request failed: ${response.status}`)
  }
  return response.json()
}

export async function registerUser(payload) {
  return request('/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
}

export async function loginUser(payload) {
  const form = new URLSearchParams()
  form.set('username', payload.username)
  form.set('password', payload.password)

  return request('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form
  })
}

export async function fetchMe(token) {
  return request('/api/v1/auth/me', {
    headers: buildHeaders(token)
  })
}

export async function fetchTodos(token, done) {
  const query = new URLSearchParams({ limit: '100', offset: '0' })
  if (done === true) query.set('done', 'true')
  if (done === false) query.set('done', 'false')

  return request(`/api/v1/todos?${query.toString()}`, {
    headers: buildHeaders(token)
  })
}

export async function createTodo(token, title) {
  return request('/api/v1/todos', {
    method: 'POST',
    headers: buildHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ title })
  })
}

<script setup>
import { computed, onMounted, ref } from 'vue'
import { createTodo, fetchMe, fetchTodos, loginUser, registerUser, updateTodoDone } from './api'

const token = ref(localStorage.getItem('todo_token') || '')
const currentUser = ref(null)
const todos = ref([])
const loadingTodos = ref(false)
const authLoading = ref(false)
const todoCreating = ref(false)
const updatingTodoId = ref(null)
const errorMessage = ref('')
const authMode = ref('login')
const todoFilter = ref('open')

const authForm = ref({ username: '', password: '' })
const todoTitle = ref('')

const isLoggedIn = computed(() => Boolean(token.value))

const filteredLabel = computed(() => {
  if (todoFilter.value === 'all') return '全部'
  if (todoFilter.value === 'done') return '已完成'
  return '进行中'
})

const openCount = computed(() => todos.value.filter((item) => !item.done).length)
const doneCount = computed(() => todos.value.filter((item) => item.done).length)

function setError(message) {
  errorMessage.value = message
  setTimeout(() => {
    if (errorMessage.value === message) {
      errorMessage.value = ''
    }
  }, 3000)
}

function saveToken(value) {
  token.value = value
  localStorage.setItem('todo_token', value)
}

function clearSession() {
  token.value = ''
  currentUser.value = null
  todos.value = []
  localStorage.removeItem('todo_token')
}

async function loadTodos() {
  if (!token.value) return
  loadingTodos.value = true
  try {
    let doneValue = null
    if (todoFilter.value === 'open') doneValue = false
    if (todoFilter.value === 'done') doneValue = true

    const response = await fetchTodos(token.value, doneValue)
    todos.value = response.items
  } catch (error) {
    if (String(error.message).includes('401')) {
      clearSession()
    }
    setError(error.message)
  } finally {
    loadingTodos.value = false
  }
}

async function bootstrap() {
  if (!token.value) return
  try {
    currentUser.value = await fetchMe(token.value)
    await loadTodos()
  } catch {
    clearSession()
  }
}

async function submitAuth() {
  authLoading.value = true
  try {
    if (authMode.value === 'register') {
      await registerUser(authForm.value)
      authMode.value = 'login'
    }

    const loginResult = await loginUser(authForm.value)
    saveToken(loginResult.access_token)
    currentUser.value = await fetchMe(loginResult.access_token)
    authForm.value.password = ''
    await loadTodos()
  } catch (error) {
    setError(error.message)
  } finally {
    authLoading.value = false
  }
}

async function submitTodo() {
  const title = todoTitle.value.trim()
  if (!title) return

  todoCreating.value = true
  try {
    await createTodo(token.value, title)
    todoTitle.value = ''
    await loadTodos()
  } catch (error) {
    setError(error.message)
  } finally {
    todoCreating.value = false
  }
}

async function toggleDone(item) {
  if (updatingTodoId.value !== null) return

  updatingTodoId.value = item.id
  try {
    await updateTodoDone(token.value, item.id, !item.done)
    await loadTodos()
  } catch (error) {
    setError(error.message)
  } finally {
    updatingTodoId.value = null
  }
}

function logout() {
  clearSession()
}

onMounted(bootstrap)
</script>

<template>
  <div class="page-shell">
    <main class="app-card">
      <section class="header-row">
        <div>
          <p class="eyebrow">Todo Lite</p>
          <h1>待办清单</h1>
          <p class="subtle">简洁记录，轻量完成。</p>
        </div>
        <button v-if="isLoggedIn" class="ghost-btn" @click="logout">退出</button>
      </section>

      <p v-if="errorMessage" class="error-tip">{{ errorMessage }}</p>

      <section v-if="!isLoggedIn" class="surface auth-surface">
        <div class="mode-tabs">
          <button class="tab-btn" :class="{ active: authMode === 'login' }" @click="authMode = 'login'">
            登录
          </button>
          <button class="tab-btn" :class="{ active: authMode === 'register' }" @click="authMode = 'register'">
            注册
          </button>
        </div>

        <form class="auth-form" @submit.prevent="submitAuth">
          <label>
            用户名
            <input v-model.trim="authForm.username" minlength="3" maxlength="50" required />
          </label>
          <label>
            密码
            <input
              v-model="authForm.password"
              type="password"
              minlength="8"
              maxlength="128"
              required
            />
          </label>
          <button class="primary-btn" :disabled="authLoading">
            {{ authLoading ? '处理中...' : authMode === 'login' ? '登录' : '注册并登录' }}
          </button>
        </form>
      </section>

      <section v-else class="content-stack">
        <section class="surface info-surface">
          <p class="welcome">你好，{{ currentUser?.username }}</p>
          <div class="stats-row">
            <article>
              <span>进行中</span>
              <strong>{{ openCount }}</strong>
            </article>
            <article>
              <span>已完成</span>
              <strong>{{ doneCount }}</strong>
            </article>
          </div>
        </section>

        <section class="surface">
          <form class="todo-create" @submit.prevent="submitTodo">
            <input
              v-model="todoTitle"
              maxlength="120"
              placeholder="添加一个待办事项"
              :disabled="todoCreating"
              required
            />
            <button class="primary-btn" :disabled="todoCreating">
              {{ todoCreating ? '添加中...' : '添加' }}
            </button>
          </form>
        </section>

        <section class="surface">
          <div class="list-header">
            <div class="mode-tabs compact">
              <button class="tab-btn" :class="{ active: todoFilter === 'all' }" @click="todoFilter = 'all'; loadTodos()">
                全部
              </button>
              <button class="tab-btn" :class="{ active: todoFilter === 'open' }" @click="todoFilter = 'open'; loadTodos()">
                进行中
              </button>
              <button class="tab-btn" :class="{ active: todoFilter === 'done' }" @click="todoFilter = 'done'; loadTodos()">
                已完成
              </button>
            </div>
            <small>{{ filteredLabel }} · {{ todos.length }} 项</small>
          </div>

          <ul v-if="!loadingTodos && todos.length" class="todo-list">
            <li
              v-for="item in todos"
              :key="item.id"
              class="todo-item"
              :class="{ done: item.done, disabled: updatingTodoId === item.id }"
            >
              <button
                class="check-btn"
                :class="{ checked: item.done }"
                :disabled="updatingTodoId !== null"
                @click="toggleDone(item)"
              >
                <span class="check-mark">✓</span>
              </button>
              <span class="title">{{ item.title }}</span>
            </li>
          </ul>

          <div v-else class="empty-state">
            {{ loadingTodos ? '正在加载...' : '还没有待办，先添加一条吧。' }}
          </div>
        </section>
      </section>
    </main>
  </div>
</template>

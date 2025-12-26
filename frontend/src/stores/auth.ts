// stores/auth.ts - Authentication store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserData, UserLogin, AuthResponse } from '@/types'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin = computed(() => user.value?.role?.toLowerCase() === 'admin')
  const isRenter = computed(() => user.value?.role?.toLowerCase() === 'renter')
  const isSeeker = computed(() => user.value?.role?.toLowerCase() === 'seeker')
  const fullName = computed(() =>
    user.value ? `${user.value.first_name} ${user.value.last_name}` : ''
  )

  // Initialize from localStorage
  const initializeAuth = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedRefreshToken = localStorage.getItem('refresh_token')
    const storedUser = localStorage.getItem('user')

    if (storedToken) accessToken.value = storedToken
    if (storedRefreshToken) refreshToken.value = storedRefreshToken
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch (e) {
        console.error('Failed to parse stored user:', e)
      }
    }

    // Set auth header if token exists
    if (accessToken.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
    }
  }

  // Save to localStorage
  const persistAuth = (authData: AuthResponse) => {
    accessToken.value = authData.access_token
    refreshToken.value = authData.refresh_token
    user.value = authData.user

    localStorage.setItem('access_token', authData.access_token)
    localStorage.setItem('refresh_token', authData.refresh_token)
    localStorage.setItem('user', JSON.stringify(authData.user))

    api.defaults.headers.common['Authorization'] = `Bearer ${authData.access_token}`
  }

  // Clear auth data
  const clearAuth = () => {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    error.value = null

    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')

    delete api.defaults.headers.common['Authorization']
  }

  // Login
  const login = async (credentials: UserLogin): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      // Step 1: Get tokens from login endpoint
      const tokenResponse = await api.post('/auth/login', credentials)
      const tokens = tokenResponse.data

      // Store tokens and set auth header
      accessToken.value = tokens.access_token
      refreshToken.value = tokens.refresh_token
      localStorage.setItem('access_token', tokens.access_token)
      if (tokens.refresh_token) {
        localStorage.setItem('refresh_token', tokens.refresh_token)
      }
      api.defaults.headers.common['Authorization'] = `Bearer ${tokens.access_token}`

      // Step 2: Fetch user data with the new token
      const userResponse = await api.get<User>('/auth/me')
      user.value = userResponse.data
      localStorage.setItem('user', JSON.stringify(userResponse.data))

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      clearAuth()
      return false
    } finally {
      loading.value = false
    }
  }

  // Register
  const register = async (userData: UserData): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      // Step 1: Register the user
      await api.post('/auth/register', userData)

      // Step 2: Auto-login with the same credentials
      const loginSuccess = await login({
        email: userData.email,
        password: userData.password
      })

      if (!loginSuccess) {
        error.value = 'Registration successful but auto-login failed. Please log in manually.'
        return false
      }

      return true
    } catch (err: any) {
      if (err.response?.data?.detail) {
        if (typeof err.response.data.detail === 'object' && err.response.data.detail.errors) {
          // Handle validation errors from backend
          const errors = err.response.data.detail.errors
          error.value = Object.values(errors).flat().join('. ')
        } else if (Array.isArray(err.response.data.detail)) {
          error.value = err.response.data.detail.map((e: any) => e.msg).join('. ')
        } else if (typeof err.response.data.detail === 'string') {
          error.value = err.response.data.detail
        } else {
          error.value = 'Registration failed'
        }
      } else {
        error.value = 'Registration failed'
      }
      return false
    } finally {
      loading.value = false
    }
  }

  // Logout
  const logout = () => {
    clearAuth()
  }

  // Refresh token
  const refreshAccessToken = async (): Promise<boolean> => {
    if (!refreshToken.value) return false

    try {
      const response = await api.post('/auth/refresh', {
        refresh_token: refreshToken.value
      })

      accessToken.value = response.data.access_token
      localStorage.setItem('access_token', response.data.access_token)
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`

      return true
    } catch (err) {
      clearAuth()
      return false
    }
  }

  // Fetch current user
  const fetchCurrentUser = async (): Promise<boolean> => {
    if (!accessToken.value) return false

    try {
      const response = await api.get<User>('/auth/me')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return true
    } catch (err) {
      return false
    }
  }

  // Update profile
  const updateProfile = async (data: Partial<User>): Promise<boolean> => {
    if (!user.value) return false

    loading.value = true
    error.value = null

    try {
      const response = await api.put<User>(`/users/${user.value.id}`, data)
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Update failed'
      return false
    } finally {
      loading.value = false
    }
  }

  // Request password reset
  const requestPasswordReset = async (email: string): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      await api.post('/auth/request-password-reset', { email })
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Password reset request failed'
      return false
    } finally {
      loading.value = false
    }
  }

  // Confirm password reset
  const confirmPasswordReset = async (token: string, newPassword: string): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      await api.post('/auth/reset-password', { token, new_password: newPassword })
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Password reset failed'
      return false
    } finally {
      loading.value = false
    }
  }

  // Check password strength
  const checkPasswordStrength = async (password: string): Promise<{
    score: number
    strength: string
    suggestions: string[]
    is_acceptable: boolean
  } | null> => {
    try {
      const response = await api.post('/auth/check-password-strength', { password })
      return response.data
    } catch (err) {
      return null
    }
  }

  // Get profile completeness
  const getProfileCompleteness = async (): Promise<number | null> => {
    try {
      const response = await api.get('/auth/profile-completeness')
      return response.data.completeness || response.data
    } catch (err) {
      return null
    }
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    // Getters
    isAuthenticated,
    isAdmin,
    isRenter,
    isSeeker,
    fullName,
    // Actions
    initializeAuth,
    login,
    register,
    logout,
    refreshAccessToken,
    fetchCurrentUser,
    updateProfile,
    requestPasswordReset,
    confirmPasswordReset,
    checkPasswordStrength,
    getProfileCompleteness,
    clearAuth
  }
})

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(
            `${api.defaults.baseURL}/auth/refresh`,
            { refresh_token: refreshToken }
          )

          const newToken = response.data.access_token
          localStorage.setItem('access_token', newToken)
          api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
          originalRequest.headers.Authorization = `Bearer ${newToken}`

          return api(originalRequest)
        } catch (refreshError) {
          // Refresh failed, clear auth
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          delete api.defaults.headers.common['Authorization']

          // Redirect to login
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api
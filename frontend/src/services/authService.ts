import api from './api'

export const registerUser = async(userData) => {
    const response = await api.post("/auth/register", userData)
    return response.data
}
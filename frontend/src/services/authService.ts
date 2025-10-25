import api from './api'
import type { userData, userLogin } from '../types/userType'

export const registerUser = async(userData: userData) => {
    const response = await api.post("/auth/register", userData)
    return response.data
}


export const loginUser = async(userLogin: userLogin) => {
    const response = await api.post("/auth/login", userLogin)
    return response.data
}
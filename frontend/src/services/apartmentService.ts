import api from './api'
import type { apartmentData } from '../types/apartmentType'

export const createApartment = async (apartmentData: apartmentData) => {
    const response = await api.post('/apartments', apartmentData)
    return response.data
}

export const listApartments = async () => {
    const response = await api.get('/apartments')
    return response.data
}
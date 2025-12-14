export interface apartmentData {
    title: string;
    description: string;
    location: string;
    apartment_type: string;
    rent_per_week: number;
    start_date: string;
    duration_len: number | null;
    place_accept: string;
    furnishing_type: string;
    is_pathroom_solo: boolean;
    parking_type: string;
    keywords: string[];
    is_active: boolean;
    images: string[];
    renter_id: number;
    created_at: string;
    updated_at: string;
}

export const createEmptyApartmentData = (): apartmentData => ({
    title: "",
    description: "",
    location: "",
    apartment_type: "",
    rent_per_week: 0,
    start_date: "",
    duration_len: null,
    place_accept: "",
    furnishing_type: "",
    is_pathroom_solo: false,
    parking_type: "",
    keywords: [],
    is_active: true,
    images: [],
    renter_id: 0,
    created_at: "",
    updated_at: "",
})
// types/userType.ts
export interface userData {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    location: string;
    flatmate_pref?: string[]; 
    keywords?: string[]; 
    role?: string;
}

export const createEmptyUserData = (): userData => ({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    location: "",
    flatmate_pref: [],
    keywords: [],
    role: "seeker",
});
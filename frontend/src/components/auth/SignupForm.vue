<template>
    <div class="max-w-md mx-auto p-6">
        <h2 class="text-2xl font-semibold mb-4">Create account</h2>

        <p v-if="successMsg" class="mb-3 rounded bg-green-100 text-green-800 px-3 py-2 text-sm">{{successMsg}}</p>
        <p v-if="errorMsg" class="mb-3 rounded bg-red-100 text-red-800 px-3 py-2 text-sm">{{errorMsg}}</p>

        <form @submit.prevent="handleSignup" class="space-y-4">
            <div>
                <label for="first_name" class="block text-sm font-medium mb-1">First Name</label>
                <input v-model="formData.first_name" id="first_name"formData required class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"/>
            </div>

            <div>
                <label for="last_name" class="block text-sm font-medium mb-1">Last Name</label>
                <input v-model="formData.last_name" id="last_name"formData required class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400" />
            </div>

            <div>
                <label for="email" class="block text-sm font-medium mb-1">Email</label>
                <input v-model="formData.email" id="email" required class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400" />
            </div>

            <div>
                <label for="password" class="block text-sm font-medium mb-1">Password</label>
                <input v-model="formData.password" id="password" required class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400" />
            </div>

            <div>
                <label for="location" class="block text-sm font-medium mb-1">Location</label>
                <input v-model="formData.location" id="location"formData class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400" />
            </div>

            <div>
            <label for="flatmate_pref" class="block text-sm font-medium mb-1">
                Flatmate Preferences
            </label>
            <select
                v-model="formData.flatmate_pref"
                id="flatmate_pref"
                multiple
                class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            >
                <option value="non-smoker">Non-smoker</option>
                <option value="student">Student</option>
                <option value="pet-friendly">Pet Friendly</option>
                <option value="quiet">Quiet</option>
                <option value="party-friendly">Party Friendly</option>
            </select>
            </div>

            <div>
            <label for="keywords" class="block text-sm font-medium mb-1">
                Keywords
            </label>
            <select
                v-model="formData.keywords"
                id="keywords"
                multiple
                class="w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            >
                <option value="gym">Gym</option>
                <option value="cooking">Cooking</option>
                <option value="music">Music</option>
                <option value="travel">Travel</option>
                <option value="clean">Clean</option>
            </select>
            </div>


            <div>
                <label for="role" class="block text-sm font-medium mb-1">Role</label>
                <select v-model="formData.role" id="role" class="w-full rounded border border-gray-300 px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-primary-400">
                <option value="seeker">Seeker</option>
                <option value="renter">Renter</option>
                </select>
            </div>

            <button type="submit" :disabled="loading" class="w-full rounded bg-orange text-white py-2 font-medium disabled:opacity-50 disabled:cursor-not-allowed">
                {{ loading ? "creating Account...": "Sign Up"}}
            </button>

        </form>

    </div>
</template>

<script setup lang="ts">
import {reactive, ref} from "vue";
import { registerUser } from "../../services/authService";
import {userData} from "../../types/authType";

//================================ Reactive variables ===============================
const formData = reactive<userData>({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  location: "",
  flatmate_pref: [],
  keywords: [],
  role: "seeker",
});

//================================ Methods ===============================
const loading = ref(false)
const successMsg = ref("")
const errorMsg = ref("")

// Submit handler
const handleSignup = async () => {
    loading.value = true
    successMsg.value = ""
    errorMsg.value = ""

    try{
        const data = await registerUser(formData)
        successMsg.value = data.message || "User created successfully!"
        Object.keys(formData).forEach((key) => (formData[key]=""))
    } catch (error) {
        errorMsg.value = error.response?.data?.detail || "Something went wrong. please try again."
    } finally {
        loading.value = false;
    }
}


</script>
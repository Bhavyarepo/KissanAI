<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <div class="mx-auto h-12 w-12 bg-green-600 rounded-full flex items-center justify-center">
          <span class="text-white font-bold text-xl">AI</span>
        </div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          {{ $t('auth.register.title') }}
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          {{ $t('auth.register.subtitle') }}
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="name" class="label">{{ $t('auth.name') }}</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="input-field"
              :placeholder="$t('auth.namePlaceholder')"
            />
          </div>
          
          <div>
            <label for="email" class="label">{{ $t('auth.email') }}</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-field"
              :placeholder="$t('auth.emailPlaceholder')"
            />
          </div>
          
          <div>
            <label for="phone" class="label">{{ $t('auth.phone') }}</label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              required
              class="input-field"
              :placeholder="$t('auth.phonePlaceholder')"
            />
          </div>
          
          <div>
            <label for="location" class="label">{{ $t('auth.location') }}</label>
            <input
              id="location"
              v-model="form.location"
              type="text"
              required
              class="input-field"
              :placeholder="$t('auth.locationPlaceholder')"
            />
          </div>
          
          <div>
            <label for="state" class="label">{{ $t('auth.state') }}</label>
            <select
              id="state"
              v-model="form.state"
              required
              class="input-field"
            >
              <option value="">{{ $t('auth.selectState') }}</option>
              <option value="Andhra Pradesh">Andhra Pradesh</option>
              <option value="Arunachal Pradesh">Arunachal Pradesh</option>
              <option value="Assam">Assam</option>
              <option value="Bihar">Bihar</option>
              <option value="Chhattisgarh">Chhattisgarh</option>
              <option value="Goa">Goa</option>
              <option value="Gujarat">Gujarat</option>
              <option value="Haryana">Haryana</option>
              <option value="Himachal Pradesh">Himachal Pradesh</option>
              <option value="Jharkhand">Jharkhand</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Kerala">Kerala</option>
              <option value="Madhya Pradesh">Madhya Pradesh</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Manipur">Manipur</option>
              <option value="Meghalaya">Meghalaya</option>
              <option value="Mizoram">Mizoram</option>
              <option value="Nagaland">Nagaland</option>
              <option value="Odisha">Odisha</option>
              <option value="Punjab">Punjab</option>
              <option value="Rajasthan">Rajasthan</option>
              <option value="Sikkim">Sikkim</option>
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Telangana">Telangana</option>
              <option value="Tripura">Tripura</option>
              <option value="Uttar Pradesh">Uttar Pradesh</option>
              <option value="Uttarakhand">Uttarakhand</option>
              <option value="West Bengal">West Bengal</option>
              <option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option>
              <option value="Chandigarh">Chandigarh</option>
              <option value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</option>
              <option value="Delhi">Delhi</option>
              <option value="Jammu and Kashmir">Jammu and Kashmir</option>
              <option value="Ladakh">Ladakh</option>
              <option value="Lakshadweep">Lakshadweep</option>
              <option value="Puducherry">Puducherry</option>
            </select>
          </div>
          
          <div>
            <label for="district" class="label">{{ $t('auth.district') }}</label>
            <input
              id="district"
              v-model="form.district"
              type="text"
              required
              class="input-field"
              :placeholder="$t('auth.districtPlaceholder')"
            />
          </div>
          
          <div>
            <label for="village" class="label">{{ $t('auth.village') }} ({{ $t('auth.optional') }})</label>
            <input
              id="village"
              v-model="form.village"
              type="text"
              class="input-field"
              :placeholder="$t('auth.villagePlaceholder')"
            />
          </div>
          
          <div>
            <label for="password" class="label">{{ $t('auth.password') }}</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-field"
              :placeholder="$t('auth.passwordPlaceholder')"
            />
          </div>
          
          <div>
            <label for="confirmPassword" class="label">{{ $t('auth.confirmPassword') }}</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="input-field"
              :placeholder="$t('auth.confirmPasswordPlaceholder')"
            />
          </div>
        </div>

        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {{ $t('auth.register.success') }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ loading ? $t('auth.registering') : $t('auth.register.button') }}
          </button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            {{ $t('auth.register.haveAccount') }}
            <router-link to="/login" class="font-medium text-green-600 hover:text-green-500">
              {{ $t('auth.login.button') }}
            </router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = ref({
      name: '',
      email: '',
      phone: '',
      location: '',
      state: '',
      district: '',
      village: '',
      password: '',
      confirmPassword: ''
    })
    const loading = ref(false)
    const error = ref('')
    const success = ref(false)
    
    const handleRegister = async () => {
      if (form.value.password !== form.value.confirmPassword) {
        error.value = 'Passwords do not match'
        return
      }
      
      loading.value = true
      error.value = ''
      success.value = false
      
      const result = await authStore.register(form.value)
      
      if (result.success) {
        success.value = true
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } else {
        error.value = result.error
      }
      
      loading.value = false
    }
    
    return {
      form,
      loading,
      error,
      success,
      handleRegister
    }
  }
}
</script>






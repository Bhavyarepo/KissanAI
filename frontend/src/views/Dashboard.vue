<template>
  <div class="min-h-screen bg-transparent">
    <!-- Welcome Section -->
    <div class="bg-transparent">
      <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-extrabold text-emerald-950 tracking-tight">
          {{ $t('dashboard.welcome', { name: user?.name }) }}
        </h1>
        <p class="text-emerald-800/70 font-medium mt-1">
          {{ $t('dashboard.location', { location: user?.location, state: user?.state }) }}
        </p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="container mx-auto px-4 py-8">
      <h2 class="text-xl font-semibold mb-6 text-gray-800">{{ $t('dashboard.quickActions') }}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <router-link 
          to="/recommendations" 
          class="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="flex items-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ $t('dashboard.getRecommendations') }}</h3>
              <p class="text-sm text-gray-600">{{ $t('dashboard.getRecommendationsDesc') }}</p>
            </div>
          </div>
        </router-link>

        <router-link 
          to="/detection" 
          class="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="flex items-center">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ $t('dashboard.detectPestDisease') }}</h3>
              <p class="text-sm text-gray-600">{{ $t('dashboard.detectPestDiseaseDesc') }}</p>
            </div>
          </div>
        </router-link>

        <router-link 
          to="/market" 
          class="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="flex items-center">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ $t('dashboard.marketPrices') }}</h3>
              <p class="text-sm text-gray-600">{{ $t('dashboard.marketPricesDesc') }}</p>
            </div>
          </div>
        </router-link>

        <router-link 
          to="/notifications" 
          class="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="flex items-center">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4 19h6v-6H4v6zM4 5h6V1H4v4zM15 7h5l-5-5v5z"></path>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ $t('dashboard.notifications') }}</h3>
              <p class="text-sm text-gray-600">{{ $t('dashboard.notificationsDesc') }}</p>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent Recommendations -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4 text-gray-800">{{ $t('dashboard.recentRecommendations') }}</h3>
          <div v-if="recentRecommendations.length === 0" class="text-gray-500 text-center py-4">
            {{ $t('dashboard.noRecommendations') }}
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="rec in recentRecommendations" 
              :key="rec.id"
              class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
            >
              <div>
                <p class="font-medium text-gray-800">{{ rec.crop_name }}</p>
                <p class="text-sm text-gray-600">{{ $t('dashboard.confidence') }}: {{ rec.confidence_score }}%</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-green-600 font-medium">₹{{ rec.expected_profit }}</p>
                <p class="text-xs text-gray-500">{{ $t('dashboard.expectedProfit') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Weather Information -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4 text-gray-800">{{ $t('dashboard.weatherInfo') }}</h3>
          <div v-if="weatherData" class="space-y-4">
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('dashboard.temperature') }}</span>
              <span class="font-medium">{{ weatherData.temperature }}°C</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('dashboard.humidity') }}</span>
              <span class="font-medium">{{ weatherData.humidity }}%</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('dashboard.rainfall') }}</span>
              <span class="font-medium">{{ weatherData.rainfall }}mm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('dashboard.condition') }}</span>
              <span class="font-medium">{{ weatherData.weather_condition }}</span>
            </div>
          </div>
          <div v-else class="text-gray-500 text-center py-4">
            {{ $t('dashboard.noWeatherData') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    const recentRecommendations = ref([])
    const weatherData = ref(null)
    const loading = ref(false)
    
    const user = computed(() => authStore.user)
    
    const fetchRecentRecommendations = async () => {
      try {
        const response = await api.get('/recommendations/history')
        recentRecommendations.value = response.data.slice(0, 5)
      } catch (error) {
        console.error('Error fetching recommendations:', error)
      }
    }
    
    const fetchWeatherData = async () => {
      try {
        const response = await api.post('/weather/fetch', {
          location: user.value.location,
          state: user.value.state,
          district: user.value.district
        })
        weatherData.value = response.data
      } catch (error) {
        console.error('Error fetching weather data:', error)
      }
    }
    
    onMounted(() => {
      fetchRecentRecommendations()
      fetchWeatherData()
    })
    
    return {
      user,
      recentRecommendations,
      weatherData,
      loading
    }
  }
}
</script>






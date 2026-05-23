<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">{{ $t('market.title') }}</h1>
      
      <!-- Search Form -->
      <div class="card mb-8">
        <h2 class="text-xl font-semibold mb-4">{{ $t('market.searchPrices') }}</h2>
        <form @submit.prevent="searchPrices" class="flex gap-4">
          <div class="flex-1">
            <input
              v-model="searchCrop"
              type="text"
              :placeholder="$t('market.enterCropName')"
              class="input-field"
            />
          </div>
          <button type="submit" :disabled="loading" class="btn-primary">
            {{ loading ? $t('market.searching') : $t('market.search') }}
          </button>
        </form>
      </div>

      <!-- Market Recommendations -->
      <div v-if="marketData" class="card mb-8">
        <h2 class="text-xl font-semibold mb-4">{{ $t('market.recommendations') }}</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 class="font-semibold text-green-800">{{ $t('market.crop') }}</h3>
            <p class="text-2xl font-bold text-green-600">{{ marketData.crop_name }}</p>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 class="font-semibold text-blue-800">{{ $t('market.averagePrice') }}</h3>
            <p class="text-2xl font-bold text-blue-600">₹{{ marketData.average_price }}/kg</p>
          </div>
          
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h3 class="font-semibold text-yellow-800">{{ $t('market.trend') }}</h3>
            <p class="text-2xl font-bold text-yellow-600 capitalize">{{ marketData.price_trend }}</p>
          </div>
        </div>

        <!-- Best Markets -->
        <div v-if="marketData.best_markets.length > 0">
          <h3 class="text-lg font-semibold mb-4">{{ $t('market.bestMarkets') }}</h3>
          <div class="space-y-3">
            <div 
              v-for="(market, index) in marketData.best_markets" 
              :key="index"
              class="flex justify-between items-center p-4 bg-gray-50 rounded-lg"
            >
              <div>
                <h4 class="font-medium text-gray-800">{{ market.market_name }}</h4>
                <p class="text-sm text-gray-600">{{ market.location }}</p>
                <p class="text-xs text-gray-500">{{ new Date(market.date).toLocaleDateString() }}</p>
              </div>
              <div class="text-right">
                <p class="text-lg font-bold text-green-600">₹{{ market.price_per_kg }}/kg</p>
                <p class="text-sm text-gray-500">{{ market.quality_grade || 'N/A' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Market Trends -->
      <div v-if="trends.length > 0" class="card">
        <h2 class="text-xl font-semibold mb-4">{{ $t('market.trends') }}</h2>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ $t('market.crop') }}
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ $t('market.currentPrice') }}
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ $t('market.trend') }}
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ $t('market.dataPoints') }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="trend in trends" :key="trend.crop_name">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ trend.crop_name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  ₹{{ trend.current_price }}/kg
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span 
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium',
                      trend.trend === 'increasing' ? 'bg-green-100 text-green-800' :
                      trend.trend === 'decreasing' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    ]"
                  >
                    {{ trend.trend }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ trend.data_points }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'Market',
  setup() {
    const searchCrop = ref('')
    const marketData = ref(null)
    const trends = ref([])
    const loading = ref(false)
    
    const searchPrices = async () => {
      if (!searchCrop.value.trim()) return
      
      loading.value = true
      try {
        const response = await api.get(`/market/prices/${searchCrop.value}`)
        marketData.value = response.data
      } catch (error) {
        console.error('Error searching prices:', error)
      }
      loading.value = false
    }
    
    const fetchTrends = async () => {
      try {
        const response = await api.get('/market/trends')
        trends.value = response.data
      } catch (error) {
        console.error('Error fetching trends:', error)
      }
    }
    
    onMounted(() => {
      fetchTrends()
    })
    
    return {
      searchCrop,
      marketData,
      trends,
      loading,
      searchPrices
    }
  }
}
</script>






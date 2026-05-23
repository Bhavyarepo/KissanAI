<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">{{ $t('recommendations.title') }}</h1>
      
      <!-- Recommendation Form -->
      <div class="card mb-8">
        <h2 class="text-xl font-semibold mb-6">{{ $t('recommendations.getRecommendations') }}</h2>
        <form @submit.prevent="getRecommendations" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="label">{{ $t('recommendations.season') }}</label>
              <select v-model="form.season" required class="input-field">
                <option value="">{{ $t('recommendations.selectSeason') }}</option>
                <option value="kharif">{{ $t('recommendations.kharif') }}</option>
                <option value="rabi">{{ $t('recommendations.rabi') }}</option>
                <option value="summer">{{ $t('recommendations.summer') }}</option>
              </select>
            </div>
            <div>
              <label class="label">{{ $t('recommendations.location') }}</label>
              <input 
                v-model="form.location" 
                type="text" 
                required 
                class="input-field"
                :placeholder="$t('recommendations.locationPlaceholder')"
              />
            </div>
            <div>
              <label class="label">{{ $t('recommendations.state') }}</label>
              <select v-model="form.state" required class="input-field">
                <option value="">{{ $t('recommendations.selectState') }}</option>
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
              <label class="label">{{ $t('auth.district') }}</label>
              <input 
                v-model="form.district" 
                type="text" 
                required 
                class="input-field"
                :placeholder="$t('auth.districtPlaceholder')"
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="btn-primary"
          >
            {{ loading ? $t('recommendations.getting') : $t('recommendations.getRecommendations') }}
          </button>
        </form>
      </div>

      <!-- Results -->
      <div v-if="recommendations.length > 0" class="space-y-6">
        <h2 class="text-2xl font-semibold text-gray-800">{{ $t('recommendations.results') }}</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="rec in recommendations" 
            :key="rec.crop_name"
            class="card hover:shadow-lg transition-shadow"
          >
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-xl font-semibold text-gray-800">{{ rec.crop_name }}</h3>
              <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm">
                {{ Math.round(rec.confidence_score * 100) }}% {{ $t('recommendations.confidence') }}
              </span>
            </div>
            
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('recommendations.expectedYield') }}</span>
                <span class="font-medium">{{ rec.expected_yield }} kg/acre</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('recommendations.expectedProfit') }}</span>
                <span class="font-medium text-green-600">₹{{ rec.expected_profit }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('recommendations.sustainability') }}</span>
                <span class="font-medium">{{ Math.round(rec.sustainability_score * 100) }}%</span>
              </div>
            </div>
            
            <div v-if="rec.fertilizer_recommendation" class="mt-4 p-3 bg-blue-50 rounded-lg">
              <h4 class="font-medium text-blue-800 mb-2">{{ $t('recommendations.fertilizer') }}</h4>
              <p class="text-sm text-blue-700">{{ rec.fertilizer_recommendation.type }}</p>
              <p class="text-sm text-blue-600 mt-1">{{ rec.fertilizer_recommendation.quantity_per_acre }}</p>
            </div>

            <div v-if="rec.expert_advice" class="mt-4 p-3 bg-green-50 rounded-lg border border-green-100">
              <h4 class="font-medium text-green-800 mb-2">AI Expert Advice</h4>
              <div class="text-sm text-green-700 whitespace-pre-line">{{ rec.expert_advice }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- History -->
      <div v-if="history.length > 0" class="mt-12">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6">{{ $t('recommendations.history') }}</h2>
        <div class="card">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ $t('recommendations.crop') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ $t('recommendations.confidence') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ $t('recommendations.yield') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ $t('recommendations.profit') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ $t('recommendations.date') }}
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in history" :key="item.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ item.crop_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ Math.round(item.confidence_score * 100) }}%
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ item.expected_yield }} kg/acre
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ₹{{ item.expected_profit }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ new Date(item.created_at).toLocaleDateString() }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'Recommendations',
  setup() {
    const form = ref({
      season: '',
      location: '',
      state: '',
      district: ''
    })
    const recommendations = ref([])
    const history = ref([])
    const loading = ref(false)
    
    const getRecommendations = async () => {
      loading.value = true
      try {
        const response = await api.post('/recommendations/crops', form.value)
        recommendations.value = response.data
      } catch (error) {
        console.error('Error getting recommendations:', error)
      }
      loading.value = false
    }
    
    const fetchHistory = async () => {
      try {
        const response = await api.get('/recommendations/history')
        history.value = response.data
      } catch (error) {
        console.error('Error fetching history:', error)
      }
    }
    
    onMounted(() => {
      fetchHistory()
    })
    
    return {
      form,
      recommendations,
      history,
      loading,
      getRecommendations
    }
  }
}
</script>






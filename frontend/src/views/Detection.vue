<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">{{ $t('detection.title') }}</h1>
      
      <!-- Detection Tabs -->
      <div class="card mb-8">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              @click="activeTab = 'pest'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeTab === 'pest'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ $t('detection.pestDetection') }}
            </button>
            <button
              @click="activeTab = 'disease'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeTab === 'disease'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ $t('detection.diseaseDetection') }}
            </button>
          </nav>
        </div>

        <!-- Pest Detection -->
        <div v-if="activeTab === 'pest'" class="mt-6">
          <h2 class="text-xl font-semibold mb-4">{{ $t('detection.uploadPestImage') }}</h2>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <input
              ref="pestFileInput"
              type="file"
              accept="image/*"
              @change="handlePestFileSelect"
              class="hidden"
            />
            <div v-if="!pestFile" @click="$refs.pestFileInput.click()" class="cursor-pointer text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <p class="mt-2 text-sm text-gray-600">{{ $t('detection.clickToUpload') }}</p>
            </div>
            <div v-else class="text-center">
              <img :src="pestFilePreview" alt="Pest image" class="mx-auto h-32 w-32 object-cover rounded-lg" />
              <p class="mt-2 text-sm text-gray-600">{{ pestFile.name }}</p>
              <button @click="detectPest" :disabled="detecting" class="btn-primary mt-4">
                {{ detecting ? $t('detection.detecting') : $t('detection.detectPest') }}
              </button>
            </div>
          </div>
        </div>

        <!-- Disease Detection -->
        <div v-if="activeTab === 'disease'" class="mt-6">
          <h2 class="text-xl font-semibold mb-4">{{ $t('detection.uploadDiseaseImage') }}</h2>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <input
              ref="diseaseFileInput"
              type="file"
              accept="image/*"
              @change="handleDiseaseFileSelect"
              class="hidden"
            />
            <div v-if="!diseaseFile" @click="$refs.diseaseFileInput.click()" class="cursor-pointer text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <p class="mt-2 text-sm text-gray-600">{{ $t('detection.clickToUpload') }}</p>
            </div>
            <div v-else class="text-center">
              <img :src="diseaseFilePreview" alt="Disease image" class="mx-auto h-32 w-32 object-cover rounded-lg" />
              <p class="mt-2 text-sm text-gray-600">{{ diseaseFile.name }}</p>
              <button @click="detectDisease" :disabled="detecting" class="btn-primary mt-4">
                {{ detecting ? $t('detection.detecting') : $t('detection.detectDisease') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-8" role="alert">
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <!-- Detection Results -->
      <div v-if="detectionResult" class="card mb-8">
        <h2 class="text-xl font-semibold mb-4">{{ $t('detection.results') }}</h2>
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-3">
              <h3 class="text-lg font-medium text-blue-800">
                {{ $t('detection.detected') }}: {{ detectionResult.name }}
              </h3>
              <p class="mt-1 text-sm text-blue-700">
                {{ $t('detection.confidence') }}: {{ Math.round(detectionResult.confidence_score * 100) }}%
              </p>
              <p class="mt-1 text-sm text-blue-700">
                {{ $t('detection.severity') }}: {{ detectionResult.severity }}
              </p>
              <div v-if="detectionResult.recommended_treatment" class="mt-3">
                <h4 class="font-medium text-blue-800">{{ $t('detection.treatment') }}</h4>
                <p class="text-sm text-blue-700">{{ detectionResult.recommended_treatment }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detection History -->
      <div v-if="history.length > 0" class="card">
        <h2 class="text-xl font-semibold mb-4">{{ $t('detection.history') }}</h2>
        <div class="space-y-4">
          <div 
            v-for="item in history" 
            :key="item.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-medium text-gray-800">
                  {{ item.pest_type || item.disease_type }}
                </h3>
                <p class="text-sm text-gray-600">
                  {{ $t('detection.confidence') }}: {{ Math.round(item.confidence_score * 100) }}%
                </p>
                <p class="text-sm text-gray-600">
                  {{ $t('detection.severity') }}: {{ item.severity }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ new Date(item.created_at).toLocaleDateString() }}
                </p>
              </div>
              <div v-if="item.recommended_treatment" class="text-right">
                <p class="text-sm text-blue-600">{{ item.recommended_treatment }}</p>
              </div>
            </div>
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
  name: 'Detection',
  setup() {
    const activeTab = ref('pest')
    const pestFile = ref(null)
    const pestFilePreview = ref('')
    const diseaseFile = ref(null)
    const diseaseFilePreview = ref('')
    const detectionResult = ref(null)
    const history = ref([])
    const detecting = ref(false)
    const error = ref('')
    
    const handlePestFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        pestFile.value = file
        error.value = ''
        const reader = new FileReader()
        reader.onload = (e) => {
          pestFilePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const handleDiseaseFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        diseaseFile.value = file
        error.value = ''
        const reader = new FileReader()
        reader.onload = (e) => {
          diseaseFilePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const detectPest = async () => {
      if (!pestFile.value) return
      
      detecting.value = true
      error.value = ''
      detectionResult.value = null
      const formData = new FormData()
      formData.append('file', pestFile.value)
      
      try {
        const response = await api.post('/detection/pest', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        detectionResult.value = response.data
        fetchHistory()
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error detecting pest'
      }
      detecting.value = false
    }
    
    const detectDisease = async () => {
      if (!diseaseFile.value) return
      
      detecting.value = true
      error.value = ''
      detectionResult.value = null
      const formData = new FormData()
      formData.append('file', diseaseFile.value)
      
      try {
        const response = await api.post('/detection/disease', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        detectionResult.value = response.data
        fetchHistory()
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error detecting disease'
      }
      detecting.value = false
    }
    
    const fetchHistory = async () => {
      try {
        const [pestResponse, diseaseResponse] = await Promise.all([
          api.get('/detection/pest/history'),
          api.get('/detection/disease/history')
        ])
        
        const pestHistory = pestResponse.data.map(item => ({ ...item, type: 'pest' }))
        const diseaseHistory = diseaseResponse.data.map(item => ({ ...item, type: 'disease' }))
        
        history.value = [...pestHistory, ...diseaseHistory]
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      } catch (error) {
        console.error('Error fetching history:', error)
      }
    }
    
    onMounted(() => {
      fetchHistory()
    })
    
    return {
      activeTab,
      pestFile,
      pestFilePreview,
      diseaseFile,
      diseaseFilePreview,
      detectionResult,
      history,
      detecting,
      error,
      handlePestFileSelect,
      handleDiseaseFileSelect,
      detectPest,
      detectDisease
    }
  }
}
</script>






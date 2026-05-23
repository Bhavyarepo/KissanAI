<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">{{ $t('notifications.title') }}</h1>
      
      <!-- Send Notification Form -->
      <div class="card mb-8">
        <h2 class="text-xl font-semibold mb-4">{{ $t('notifications.sendNotification') }}</h2>
        <form @submit.prevent="sendNotification" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label">{{ $t('notifications.message') }}</label>
              <textarea
                v-model="form.message"
                required
                rows="3"
                class="input-field"
                :placeholder="$t('notifications.messagePlaceholder')"
              ></textarea>
            </div>
            <div class="space-y-4">
              <div>
                <label class="label">{{ $t('notifications.type') }}</label>
                <select v-model="form.notification_type" required class="input-field">
                  <option value="">{{ $t('notifications.selectType') }}</option>
                  <option value="weather">{{ $t('notifications.weather') }}</option>
                  <option value="market">{{ $t('notifications.market') }}</option>
                  <option value="reminder">{{ $t('notifications.reminder') }}</option>
                </select>
              </div>
              <div>
                <label class="label">{{ $t('notifications.priority') }}</label>
                <select v-model="form.priority" class="input-field">
                  <option value="low">{{ $t('notifications.low') }}</option>
                  <option value="medium">{{ $t('notifications.medium') }}</option>
                  <option value="high">{{ $t('notifications.high') }}</option>
                </select>
              </div>
            </div>
          </div>
          
          <button type="submit" :disabled="loading" class="btn-primary">
            {{ loading ? $t('notifications.sending') : $t('notifications.send') }}
          </button>
        </form>
      </div>

      <!-- Quick Alerts -->
      <div class="card mb-8">
        <h2 class="text-xl font-semibold mb-4">{{ $t('notifications.quickAlerts') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button 
            @click="sendWeatherAlert('rain')"
            :disabled="loading"
            class="p-4 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
                </svg>
              </div>
              <div class="text-left">
                <h3 class="font-medium text-gray-800">{{ $t('notifications.rainAlert') }}</h3>
                <p class="text-sm text-gray-600">{{ $t('notifications.rainAlertDesc') }}</p>
              </div>
            </div>
          </button>

          <button 
            @click="sendWeatherAlert('drought')"
            :disabled="loading"
            class="p-4 border border-orange-200 rounded-lg hover:bg-orange-50 transition-colors"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                </svg>
              </div>
              <div class="text-left">
                <h3 class="font-medium text-gray-800">{{ $t('notifications.droughtAlert') }}</h3>
                <p class="text-sm text-gray-600">{{ $t('notifications.droughtAlertDesc') }}</p>
              </div>
            </div>
          </button>

          <button 
            @click="sendWeatherAlert('storm')"
            :disabled="loading"
            class="p-4 border border-red-200 rounded-lg hover:bg-red-50 transition-colors"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
                </svg>
              </div>
              <div class="text-left">
                <h3 class="font-medium text-gray-800">{{ $t('notifications.stormAlert') }}</h3>
                <p class="text-sm text-gray-600">{{ $t('notifications.stormAlertDesc') }}</p>
              </div>
            </div>
          </button>

          <button 
            @click="sendMarketAlert()"
            :disabled="loading"
            class="p-4 border border-green-200 rounded-lg hover:bg-green-50 transition-colors"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                </svg>
              </div>
              <div class="text-left">
                <h3 class="font-medium text-gray-800">{{ $t('notifications.marketAlert') }}</h3>
                <p class="text-sm text-gray-600">{{ $t('notifications.marketAlertDesc') }}</p>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Notification History -->
      <div v-if="notifications.length > 0" class="card">
        <h2 class="text-xl font-semibold mb-4">{{ $t('notifications.history') }}</h2>
        <div class="space-y-4">
          <div 
            v-for="notification in notifications" 
            :key="notification.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <div class="flex items-center mb-2">
                  <span 
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium mr-2',
                      notification.notification_type === 'weather' ? 'bg-blue-100 text-blue-800' :
                      notification.notification_type === 'market' ? 'bg-green-100 text-green-800' :
                      'bg-gray-100 text-gray-800'
                    ]"
                  >
                    {{ notification.notification_type }}
                  </span>
                  <span 
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium',
                      notification.priority === 'high' ? 'bg-red-100 text-red-800' :
                      notification.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    ]"
                  >
                    {{ notification.priority }}
                  </span>
                </div>
                <p class="text-gray-800 mb-2">{{ notification.message }}</p>
                <div class="flex items-center text-sm text-gray-500">
                  <span>{{ new Date(notification.created_at).toLocaleDateString() }}</span>
                  <span v-if="notification.is_sent" class="ml-4 text-green-600">
                    ✓ {{ $t('notifications.sent') }}
                  </span>
                  <span v-else class="ml-4 text-red-600">
                    ✗ {{ $t('notifications.notSent') }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="card text-center py-8">
        <p class="text-gray-500">{{ $t('notifications.noNotifications') }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'Notifications',
  setup() {
    const form = ref({
      message: '',
      notification_type: '',
      priority: 'medium'
    })
    const notifications = ref([])
    const loading = ref(false)
    
    const sendNotification = async () => {
      loading.value = true
      try {
        await api.post('/notifications/send', form.value)
        form.value = {
          message: '',
          notification_type: '',
          priority: 'medium'
        }
        fetchNotifications()
      } catch (error) {
        console.error('Error sending notification:', error)
      }
      loading.value = false
    }
    
    const sendWeatherAlert = async (alertType) => {
      loading.value = true
      try {
        await api.post('/notifications/weather-alert', {
          location: 'Your Location',
          alert_type: alertType
        })
        fetchNotifications()
      } catch (error) {
        console.error('Error sending weather alert:', error)
      }
      loading.value = false
    }
    
    const sendMarketAlert = async () => {
      loading.value = true
      try {
        await api.post('/notifications/market-alert', {
          crop_name: 'Rice',
          price_change: 'increased by 15%'
        })
        fetchNotifications()
      } catch (error) {
        console.error('Error sending market alert:', error)
      }
      loading.value = false
    }
    
    const fetchNotifications = async () => {
      try {
        const response = await api.get('/notifications/history')
        notifications.value = response.data
      } catch (error) {
        console.error('Error fetching notifications:', error)
      }
    }
    
    onMounted(() => {
      fetchNotifications()
    })
    
    return {
      form,
      notifications,
      loading,
      sendNotification,
      sendWeatherAlert,
      sendMarketAlert
    }
  }
}
</script>






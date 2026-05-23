<template>
  <nav class="bg-white/90 backdrop-blur-md shadow-sm border-b border-green-100 sticky top-0 z-50">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center py-4">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
              <span class="text-white font-bold text-sm">AI</span>
            </div>
            <span class="text-xl font-bold text-emerald-900">{{ t('app.title') }}</span>
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-6">
          <router-link 
            v-if="!isAuthenticated" 
            to="/" 
            class="text-gray-600 hover:text-gray-800 transition-colors"
          >
            {{ t('nav.home') }}
          </router-link>
          
          <router-link 
            v-if="isAuthenticated" 
            to="/dashboard" 
            class="text-gray-600 hover:text-gray-800 transition-colors"
          >
            {{ t('nav.dashboard') }}
          </router-link>
          
          <router-link 
            v-if="isAuthenticated" 
            to="/recommendations" 
            class="text-gray-600 hover:text-gray-800 transition-colors"
          >
            {{ t('nav.recommendations') }}
          </router-link>
          
          <router-link 
            v-if="isAuthenticated" 
            to="/detection" 
            class="text-gray-600 hover:text-gray-800 transition-colors"
          >
            {{ t('nav.detection') }}
          </router-link>
          
          <router-link 
            v-if="isAuthenticated" 
            to="/market" 
            class="text-gray-600 hover:text-gray-800 transition-colors"
          >
            {{ t('nav.market') }}
          </router-link>
        </div>

        <!-- Language Selector -->
        <div class="flex items-center space-x-4">
          <select 
            v-model="currentLocale" 
            @change="changeLanguage"
            class="text-sm border border-gray-300 rounded px-2 py-1"
          >
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="te">తెలుగు</option>
          </select>

          <!-- Auth Buttons -->
          <div v-if="!isAuthenticated" class="flex items-center space-x-2">
            <router-link 
              to="/login" 
              class="text-gray-600 hover:text-gray-800 transition-colors"
            >
              {{ t('nav.login') }}
            </router-link>
            <router-link 
              to="/register" 
              class="btn-primary"
            >
              {{ t('nav.register') }}
            </router-link>
          </div>

          <!-- User Menu -->
          <div v-else class="flex items-center space-x-4">
            <span class="text-gray-600">{{ user?.name }}</span>
            <button 
              @click="logout" 
              class="text-gray-600 hover:text-gray-800 transition-colors"
            >
              {{ t('nav.logout') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'NavBar',
  setup() {
    const router = useRouter()
    const { t, locale } = useI18n()   // <-- include `t` here
    const authStore = useAuthStore()
    
    const currentLocale = ref(locale.value)
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)
    
    const changeLanguage = () => {
      locale.value = currentLocale.value
    }
    
    const logout = () => {
      authStore.logout()
      router.push('/')
    }
    
    return {
      t,              // <-- return it to use in template
      currentLocale,
      isAuthenticated,
      user,
      changeLanguage,
      logout
    }
  }
}
</script>



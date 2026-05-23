<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-emerald-900/10 -z-10"></div>
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl md:text-7xl font-extrabold mb-8 text-emerald-950 tracking-tight">
          {{ $t('home.hero.title') }}
        </h1>
        <p class="text-xl md:text-2xl mb-12 max-w-3xl mx-auto text-emerald-800/80 leading-relaxed">
          {{ $t('home.hero.subtitle') }}
        </p>
        <div class="flex flex-col sm:flex-row gap-6 justify-center">
          <router-link 
            to="/register" 
            class="bg-emerald-600 text-white px-10 py-4 rounded-2xl font-bold shadow-lg shadow-emerald-200 hover:bg-emerald-700 transition-all transform hover:-translate-y-1"
          >
            {{ $t('home.hero.getStarted') }}
          </router-link>
          <router-link 
            to="/login" 
            class="bg-white text-emerald-700 border border-emerald-100 px-10 py-4 rounded-2xl font-bold shadow-sm hover:shadow-md transition-all transform hover:-translate-y-1"
          >
            {{ $t('home.hero.login') }}
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">
          {{ $t('home.features.title') }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="card text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-3">{{ $t('home.features.cropRecommendation.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.features.cropRecommendation.description') }}</p>
          </div>

          <div class="card text-center">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-3">{{ $t('home.features.detection.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.features.detection.description') }}</p>
          </div>

          <div class="card text-center">
            <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-3">{{ $t('home.features.market.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.features.market.description') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="py-16 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">
          {{ $t('home.howItWorks.title') }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">1</div>
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.howItWorks.step1.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.howItWorks.step1.description') }}</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">2</div>
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.howItWorks.step2.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.howItWorks.step2.description') }}</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">3</div>
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.howItWorks.step3.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.howItWorks.step3.description') }}</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">4</div>
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.howItWorks.step4.title') }}</h3>
            <p class="text-gray-600">{{ $t('home.howItWorks.step4.description') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-16 bg-green-600 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-4">{{ $t('home.cta.title') }}</h2>
        <p class="text-xl mb-8">{{ $t('home.cta.description') }}</p>
        <router-link 
          to="/register" 
          class="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
        >
          {{ $t('home.cta.button') }}
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>






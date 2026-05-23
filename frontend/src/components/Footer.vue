<template>
  <footer class="bg-gray-800 text-white py-8 mt-16">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Company Info -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ $t('footer.company') }}</h3>
          <p class="text-gray-300 text-sm">
            {{ $t('footer.description') }}
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ $t('footer.quickLinks') }}</h3>
          <ul class="space-y-2">
            <li><router-link to="/" class="text-gray-300 hover:text-white transition-colors">{{ $t('nav.home') }}</router-link></li>
            <li><router-link to="/recommendations" class="text-gray-300 hover:text-white transition-colors">{{ $t('nav.recommendations') }}</router-link></li>
            <li><router-link to="/detection" class="text-gray-300 hover:text-white transition-colors">{{ $t('nav.detection') }}</router-link></li>
            <li><router-link to="/market" class="text-gray-300 hover:text-white transition-colors">{{ $t('nav.market') }}</router-link></li>
          </ul>
        </div>

        <!-- Support -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ $t('footer.support') }}</h3>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-300 hover:text-white transition-colors">{{ $t('footer.help') }}</a></li>
            <li><a href="#" class="text-gray-300 hover:text-white transition-colors">{{ $t('footer.contact') }}</a></li>
            <li><a href="#" class="text-gray-300 hover:text-white transition-colors">{{ $t('footer.privacy') }}</a></li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ $t('footer.contact') }}</h3>
          <div class="space-y-2 text-sm text-gray-300">
            <p>Email: support@aicrop.com</p>
            <p>Phone: +91 9876543210</p>
            <p>{{ $t('footer.address') }}</p>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300 text-sm">
        <p>&copy; 2026 copyright by bhavya anand. KissanAi. {{ $t('footer.rights') }}</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>






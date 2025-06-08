<template>
  <nav class="px-4 md:px-8 py-4">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center space-x-2">
        <div class="w-8 h-8 text-moment-400 text-2xl">
          🌲
        </div>
        <span class="text-xl font-bold text-gray-800">MomenTree</span>
      </router-link>
      
      <!-- Desktop Navigation - Center -->
      <div class="hidden md:flex items-center space-x-8">
        <router-link 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.path" 
          class="text-gray-600 hover:text-gray-800 transition-colors"
        >
          {{ item.name }}
        </router-link>
      </div>

      <!-- Desktop Right Side -->
      <div class="hidden md:flex items-center space-x-6">
        <template v-if="isLoggedIn">
          <router-link to="/profile" class="text-gray-600 hover:text-gray-800 transition-colors">프로필</router-link>
          <button @click="handleLogout" class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-full transition-colors">
            로그아웃
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 hover:text-gray-800 transition-colors">로그인</router-link>
          <router-link to="/signup" class="bg-moment-400 hover:bg-moment-500 text-white px-6 py-2 rounded-full transition-colors">
            회원가입
          </router-link>
        </template>
      </div>

      <!-- Mobile Menu Button -->
      <button 
        @click="toggleMobileMenu"
        class="md:hidden p-2 text-gray-600"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div v-if="isMobileMenuOpen" class="md:hidden bg-white/95 backdrop-blur-sm shadow-lg rounded-lg mt-2 max-w-7xl mx-auto">
      <div class="px-4 py-2 space-y-2">
        <router-link 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.path" 
          class="block py-2 text-gray-600 hover:text-gray-800"
          @click="closeMobileMenu"
        >
          {{ item.name }}
        </router-link>
        <template v-if="isLoggedIn">
          <router-link to="/profile" class="block py-2 text-gray-600 hover:text-gray-800" @click="closeMobileMenu">프로필</router-link>
          <button @click="handleLogoutAndClose" class="w-full bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-full transition-colors mt-2 block text-center">
            로그아웃
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="block py-2 text-gray-600 hover:text-gray-800" @click="closeMobileMenu">로그인</router-link>
          <router-link to="/signup" class="w-full bg-moment-400 hover:bg-moment-500 text-white px-6 py-2 rounded-full transition-colors mt-2 block text-center" @click="closeMobileMenu">
            회원가입
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()
const isMobileMenuOpen = ref(false)
const navItems = [
  // { name: '목표 설정', path: '/goals' },
  { name: '상품 추천', path: '/recommend' },
  { name: '상품 조회', path: '/products' },
  { name: '주변 은행 찾기', path: '/bank-finder' },
  { name: '현물 상품 비교', path: '/commodities' },
  { name: '정보 검색', path: '/search' },
  { name: '커뮤니티', path: '/community' }
]

const isLoggedIn = computed(() => accountStore.isLoggedIn)

const handleLogout = async () => {
  const result = await accountStore.logOut()
  if (!result.success) {
    console.error('로그아웃 실패:', result.error)
  } 
}

const handleLogoutAndClose = async () => {
  await handleLogout()
  closeMobileMenu()
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>
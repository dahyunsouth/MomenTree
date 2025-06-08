<template>
  <div class="flex justify-center px-4 mt-16">
    <div class="bg-white rounded-3xl shadow-lg p-8 w-full max-w-md">
      <h2 class="text-2xl font-bold mb-2">로그인</h2>
      <p class="text-gray-600 mb-6">계속하려면 로그인해주세요.</p>
      
      <form @submit.prevent="login" class="space-y-4">
        <!-- ID 입력 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">ID</label>
          <input
            type="text"
            v-model="formData.id"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
            placeholder="아이디를 입력하세요"
          >
        </div>

        <!-- 비밀번호 입력 -->
        <div class="relative">
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <div class="relative">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="formData.password"
              class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
              placeholder="비밀번호를 입력하세요"
            >
            <button
              type="button"
              @click="togglePassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 로그인 상태 유지 -->
        <div class="flex items-center">
          <input
            type="checkbox"
            id="remember"
            v-model="formData.rememberMe"
            class="h-4 w-4 text-[#006775] focus:ring-[#006775] border-gray-300 rounded"
          >
          <label for="remember" class="ml-2 block text-sm text-gray-700">
            로그인 상태 유지
          </label>
        </div>

        <!-- 로그인 버튼 -->
        <button
          type="submit"
          class="w-full bg-[#4285F4] text-white py-2 px-4 rounded-lg hover:bg-[#3367D6] transition-colors"
        >
          로그인
        </button>

        <!-- 구분선 -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">or</span>
          </div>
        </div>

        <!-- 구글 로그인 -->
        <button
          type="button"
          @click="handleGoogleLogin"
          class="w-full flex items-center justify-center gap-2 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <img src="/google-icon.svg" alt="Google" class="w-5 h-5">
          Google 로그인
        </button>

        <!-- 회원가입 링크 -->
        <div class="text-center mt-6">
          <router-link to="/signup" class="text-[#4285F4] hover:underline">
            회원가입
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()
const showPassword = ref(false)

const formData = ref({
  id: '',
  password: '',
  rememberMe: false
})

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const login = async () => {
  const result = await accountStore.logIn(formData.value)
  if (!result.success) {
    // 로그인 실패 처리
    alert(result.error || '로그인에 실패했습니다.')
  }
}

const handleGoogleLogin = () => {
  // TODO: Google 로그인 로직 구현
  console.log('Google login attempt')
}
</script> 
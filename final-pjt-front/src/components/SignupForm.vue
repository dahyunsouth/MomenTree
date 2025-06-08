<template>
  <div class="flex justify-center px-4 mt-16">
    <div class="bg-white rounded-3xl shadow-lg p-8 w-full max-w-2xl">
      <h2 class="text-2xl font-bold mb-2">회원가입</h2>
      <p class="text-gray-600 mb-6">MomenTree와 함께 목표를 달성해보세요!</p>
      
      <form @submit.prevent="handleSignup" class="space-y-6">
        <!-- 기본 정보 섹션 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-gray-700">기본 정보</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- ID -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">ID</label>
              <input
                type="text"
                v-model="formData.id"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                required
              >
            </div>
            <!-- Password -->
            <div class="relative">
              <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div class="relative">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="formData.password"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                  required
                >
                <button
                  type="button"
                  @click="togglePassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path v-if="showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>
            <!-- Password Confirm -->
            <div class="relative">
              <label class="block text-sm font-medium text-gray-700 mb-1">Password 확인</label>
              <div class="relative">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="formData.passwordConfirm"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                  required
                >
              </div>
            </div>
            <!-- 이름 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">이름</label>
              <input
                type="text"
                v-model="formData.name"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                required
              >
            </div>
            <!-- 닉네임 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">닉네임</label>
              <input
                type="text"
                v-model="formData.nickname"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                required
              >
            </div>
            <!-- 이메일 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
              <input
                type="email"
                v-model="formData.email"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                required
              >
            </div>
            <!-- 나이 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">나이</label>
              <div class="relative flex items-center">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">만</span>
                <input
                  type="number"
                  v-model="formData.age"
                  class="w-full pl-8 pr-10 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  min="1"
                  required
                >
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">세</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 프로필 사진 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-gray-700">프로필 사진</h3>
          <div class="flex items-center space-x-4">
            <div class="w-24 h-24 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
              <img v-if="profilePreview" :src="profilePreview" alt="Profile Preview" class="w-full h-full object-cover">
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <input
                type="file"
                ref="fileInput"
                @change="handleFileChange"
                accept="image/*"
                class="hidden"
              >
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors"
              >
                사진 업로드
              </button>
            </div>
          </div>
        </div>

        <!-- 재무 정보 섹션 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-gray-700">재무 정보</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- 월급 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">월급</label>
              <div class="relative">
                <input
                  type="number"
                  v-model="formData.salary"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  min="0"
                  required
                >
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">만원</span>
              </div>
            </div>
            <!-- 현재 자산 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">현재 자산</label>
              <div class="relative">
                <input
                  type="number"
                  v-model="formData.wealth"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  min="0"
                  required
                >
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">만원</span>
              </div>
            </div>
            <!-- 월 납입 가능 금액 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">월 납입 가능 금액</label>
              <div class="relative">
                <input
                  type="number"
                  v-model="formData.monthlyDeposit"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  min="0"
                  required
                >
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">만원</span>
              </div>
            </div>
            <!-- 목표 기간 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">목표 기간</label>
              <div class="relative">
                <input
                  type="number"
                  v-model="formData.desirePeriod"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  min="1"
                  required
                >
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">개월</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 가입하기 버튼 -->
        <button
          type="submit"
          class="w-full bg-[#006775] text-white py-3 px-4 rounded-lg hover:bg-[#005766] transition-colors mt-8"
        >
          가입하기
        </button>

        <!-- 로그인 링크 -->
        <div class="text-center">
          <span class="text-gray-600">이미 계정이 있으신가요?</span>
          <router-link to="/login" class="text-[#006775] hover:underline ml-2">
            로그인
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
const fileInput = ref(null)
const profilePreview = ref(null)
const showPassword = ref(false)

const formData = ref({
  id: '',
  password: '',
  passwordConfirm: '',  // 비밀번호 확인용
  name: '',
  nickname: '',
  email: '',
  age: '',
  profileImage: null,
  salary: '',
  wealth: '',
  monthlyDeposit: '',
  desirePeriod: '',
  saving: [],
  deposit: []
})

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.profileImage = file
    const reader = new FileReader()
    reader.onload = (e) => {
      profilePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const validateForm = () => {
  // 필수 필드 검증
  if (!formData.value.id) {
    alert('아이디를 입력해주세요.')
    return false
  }
  if (!formData.value.password) {
    alert('비밀번호를 입력해주세요.')
    return false
  }
  if (formData.value.password !== formData.value.passwordConfirm) {
    alert('비밀번호가 일치하지 않습니다.')
    return false
  }
  if (!formData.value.name) {
    alert('이름을 입력해주세요.')
    return false
  }
  if (!formData.value.nickname) {
    alert('닉네임을 입력해주세요.')
    return false
  }
  if (!formData.value.email) {
    alert('이메일을 입력해주세요.')
    return false
  }
  if (!formData.value.age) {
    alert('나이를 입력해주세요.')
    return false
  }
  
  // 재무 정보 검증
  if (!formData.value.salary) {
    alert('월급을 입력해주세요.')
    return false
  }
  if (!formData.value.wealth) {
    alert('현재 자산을 입력해주세요.')
    return false
  }
  if (!formData.value.monthlyDeposit) {
    alert('월 납입 가능 금액을 입력해주세요.')
    return false
  }
  if (!formData.value.desirePeriod) {
    alert('목표 기간을 입력해주세요.')
    return false
  }

  return true
}

const handleSignup = async () => {
  if (!validateForm()) return

  const result = await accountStore.signUp({
    id: formData.value.id,
    password: formData.value.password,
    name: formData.value.name,
    nickname: formData.value.nickname,
    email: formData.value.email,
    age: formData.value.age,
    profileImage: formData.value.profileImage,
    salary: formData.value.salary,
    wealth: formData.value.wealth,
    monthlyDeposit: formData.value.monthlyDeposit,
    desirePeriod: formData.value.desirePeriod,
    saving: formData.value.saving,
    deposit: formData.value.deposit
  })

  if (result.success) {
    alert('회원가입이 완료되었습니다.')
    router.push({ name: 'Home' })
  } else {
    alert(result.error || '회원가입에 실패했습니다. 다시 시도해주세요.')
  }
}
</script> 
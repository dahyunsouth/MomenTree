<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-2xl mx-auto">
      <div class="bg-white/30 rounded-3xl shadow-lg p-8">
        <h1 class="text-2xl font-bold text-gray-800 mb-8">프로필 수정</h1>
        
        <form @submit.prevent="handleUpdate" class="space-y-8">
          <!-- 프로필 이미지 섹션 -->
          <div class="flex flex-col items-center space-y-4">
            <div class="relative">
              <img 
                :src="profilePreview || user.profile_image" 
                alt="프로필 이미지" 
                class="w-48 h-48 rounded-full object-cover border-4 border-[#006775]/20"
              />
              <label 
                class="absolute bottom-0 right-0 bg-[#006775] text-white p-3 rounded-full cursor-pointer hover:bg-[#005766] transition-colors"
                style="transform: translate(25%, 25%)"
              >
                <input type="file" @change="handleFileChange" accept="image/*" class="hidden" />
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </label>
            </div>
          </div>

          <!-- 개인 정보 섹션 -->
          <div class="bg-white/50 rounded-2xl p-6 shadow-sm">
            <h2 class="text-xl font-semibold mb-6 text-[#006775]">개인 정보</h2>
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">아이디</label>
                  <input 
                    type="text" 
                    v-model="user.username" 
                    disabled 
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 bg-gray-50 text-gray-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">닉네임</label>
                  <input 
                    type="text" 
                    v-model="form.nickname" 
                    required
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                  />
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
                  <input 
                    type="email" 
                    v-model="form.email" 
                    required
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">나이</label>
                  <input 
                    type="number" 
                    v-model="form.age" 
                    required
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 재무 정보 섹션 -->
          <div class="bg-white/50 rounded-2xl p-6 shadow-sm">
            <h2 class="text-xl font-semibold mb-6 text-[#006775]">재무 정보</h2>
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">월 수입</label>
                  <div class="relative">
                    <input 
                      type="number" 
                      v-model="form.salary" 
                      required
                      class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent pr-12"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">만원</span>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">총 자산</label>
                  <div class="relative">
                    <input 
                      type="number" 
                      v-model="form.wealth" 
                      required
                      class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent pr-12"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">만원</span>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">월 저축액</label>
                  <div class="relative">
                    <input 
                      type="number" 
                      v-model="form.monthly_deposit" 
                      required
                      class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent pr-12"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">만원</span>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">목표 기간</label>
                  <div class="relative">
                    <input 
                      type="number" 
                      v-model="form.desire_period" 
                      required
                      class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent pr-12"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">개월</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 버튼 그룹 -->
          <div class="flex justify-end space-x-4">
            <router-link 
              to="/profile" 
              class="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              취소
            </router-link>
            <button 
              type="submit" 
              class="px-6 py-2 bg-[#006775] text-white rounded-lg hover:bg-[#005766] transition-colors"
            >
              저장
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref({})
const form = ref({})
const profilePreview = ref(null)
const profileImage = ref(null)

const fetchProfile = async () => {
  const token = localStorage.getItem('token')
  const response = await axios.get('http://localhost:8000/accounts/profile/', {
    headers: { Authorization: `Token ${token}` }
  })
  user.value = response.data.user
  form.value = {
    nickname: user.value.nickname,
    email: user.value.email,
    age: user.value.age,
    salary: user.value.salary,
    wealth: user.value.wealth,
    monthly_deposit: user.value.monthly_deposit,
    desire_period: user.value.desire_period
  }
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    profileImage.value = file
    const reader = new FileReader()
    reader.onload = (ev) => {
      profilePreview.value = ev.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleUpdate = async () => {
  const token = localStorage.getItem('token')
  const formData = new FormData()
  formData.append('nickname', form.value.nickname)
  formData.append('email', form.value.email)
  formData.append('age', form.value.age)
  formData.append('salary', form.value.salary)
  formData.append('wealth', form.value.wealth)
  formData.append('monthlyDeposit', form.value.monthly_deposit)
  formData.append('desirePeriod', form.value.desire_period)
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }
  await axios.patch('http://localhost:8000/accounts/profile/', formData, {
    headers: {
      Authorization: `Token ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
  alert('프로필이 수정되었습니다.')
  router.push('/profile')
}

onMounted(fetchProfile)
</script>

<style scoped>
.profile-edit-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.input-disabled {
  background: #f3f3f3;
  color: #aaa;
}
.btn-save {
  background: #006775;
  color: #fff;
  padding: 0.7rem 2rem;
  border-radius: 6px;
  margin-right: 1rem;
}
.btn-cancel {
  color: #666;
  padding: 0.7rem 2rem;
  border-radius: 6px;
  background: #f3f3f3;
  text-decoration: none;
}
</style> 
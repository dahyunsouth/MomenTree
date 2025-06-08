<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-5xl mx-auto space-y-8">
      <!-- 프로필 정보 섹션 -->
      <div class="bg-white/30 rounded-3xl shadow-lg p-8">
        <!-- 프로필 헤더 -->
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center">
            <img 
              :src="getProfileImageUrl(userInfo.profile_image)" 
              :alt="userInfo.username"
              class="w-32 h-32 rounded-full object-cover border-4 border-[#006775]/20"
            >
            <div class="ml-6 flex items-center">
              <h1 class="text-4xl font-extrabold text-[#006775] leading-none tracking-tight">⭐ {{ userInfo.username }} <span class="text-gray-800">님의 프로필 ⭐</span></h1>
            </div>
          </div>
          <router-link 
            to="/profile/edit" 
            class="px-6 py-2 bg-[#006775] text-white rounded-lg hover:bg-[#005766] transition-colors text-lg font-bold self-center"
          >
            프로필 수정
          </router-link>
        </div>

        <!-- 프로필 정보 그리드 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- 개인 정보 섹션 -->
          <div class="bg-white/50 rounded-2xl p-6 shadow-sm">
            <h2 class="text-xl font-semibold mb-6 text-[#006775]">개인 정보</h2>
            <div class="space-y-6">
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">아이디</h3>
                </div>
                <p class="text-lg font-medium">{{ userInfo.username }}</p>
              </div>
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">닉네임</h3>
                </div>
                <p class="text-lg font-medium">{{ userInfo.nickname }}</p>
              </div>
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">이메일</h3>
                </div>
                <p class="text-lg font-medium">{{ userInfo.email }}</p>
              </div>
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">나이</h3>
                </div>
                <p class="text-lg font-medium">{{ userInfo.age }}세</p>
              </div>
            </div>
          </div>

          <!-- 재무 정보 섹션 -->
          <div class="bg-white/50 rounded-2xl p-6 shadow-sm">
            <h2 class="text-xl font-semibold mb-6 text-[#006775]">재무 정보</h2>
            <div class="space-y-6">
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">월 수입</h3>
                </div>
                <p class="text-lg font-medium">{{ formatCurrency(userInfo.salary) }} 만원</p>
              </div>
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">총 자산</h3>
                </div>
                <p class="text-lg font-medium">{{ formatCurrency(userInfo.wealth) }} 만원</p>
              </div>
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">월 저축액</h3>
                </div>
                <p class="text-lg font-medium">{{ formatCurrency(userInfo.monthly_deposit) }} 만원</p>
              </div>
              <div class="flex items-center">
                <div class="w-24">
                  <h3 class="text-sm font-medium text-gray-500">목표 기간</h3>
                </div>
                <p class="text-lg font-medium">{{ userInfo.desire_period }} 개월</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 관심 상품 섹션 -->
      <InterestProducts @update="onInterestUpdate" />
      <InterestProductChart v-if="interestChartData.length" :products="interestChartData" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import InterestProducts from '@/components/InterestProducts.vue'
import InterestProductChart from '@/components/InterestProductChart.vue'

const router = useRouter()
const userInfo = ref({
  username: '',
  email: '',
  salary: 0,
  wealth: 0,
  desire_period: 0,
  profile_image: ''
})

const interestChartData = ref([])

function getInterestRateRaw(product, term, prefer) {
  const options = product.depositoption_set || product.savingoption_set
  if (!options || !Array.isArray(options)) return 0
  const option = options.find(opt => Number(opt.save_trm) === Number(term))
  if (!option) return 0
  if (prefer) {
    // 우대금리가 있으면 우대금리, 없으면 기본금리
    return option.intr_rate2 && Number(option.intr_rate2) > Number(option.intr_rate)
      ? Number(option.intr_rate2)
      : Number(option.intr_rate)
  } else {
    return Number(option.intr_rate)
  }
}

function onInterestUpdate(products) {
  interestChartData.value = products.map(p => ({
    name: p.fin_prdt_nm,
    intr_rate: getInterestRateRaw(p, 12, false),   // 저축금리
    intr_rate2: getInterestRateRaw(p, 12, true)    // 최고우대금리
  }))
}

// 숫자 포맷팅 함수
const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR').format(value)
}

// 프로필 이미지 경로 보정 함수
const getProfileImageUrl = (path) => {
  if (!path) return '/default-profile.png'
  if (path.startsWith('http')) return path
  return `http://localhost:8000${path}`
}

// 사용자 정보 가져오기
const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await axios.get('http://localhost:8000/accounts/profile/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    userInfo.value = response.data.user
  } catch (error) {
    console.error('사용자 정보를 가져오는데 실패했습니다:', error)
    if (error.response?.status === 401) {
      router.push('/login')
    }
  }
}

onMounted(fetchUserInfo)
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.profile-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 2rem;
}

.profile-section {
  margin-bottom: 2rem;
}

.profile-section:last-child {
  margin-bottom: 0;
}

h1 {
  color: #333;
  margin-bottom: 2rem;
}

h2 {
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.info-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-group p {
  margin: 0;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

strong {
  color: #333;
}

.btn-edit {
  background: #006775;
  color: #fff;
  padding: 0.7rem 2rem;
  border-radius: 6px;
  text-decoration: none;
}

.favorite-products {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.product-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1rem;
  position: relative;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.product-info {
  padding: 0.5rem 0;
}

.product-info h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.price {
  font-weight: bold;
  color: #006775;
  margin-bottom: 0.5rem;
}

.description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
}

.remove-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #ff4444;
  color: white;
  border: none;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
}

.remove-btn:hover {
  background: #cc0000;
}

.no-favorites {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
}
</style> 
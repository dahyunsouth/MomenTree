<template>
  <div class="p-6 bg-white/30 rounded-3xl shadow-lg">
    <h2 class="text-2xl font-bold mb-6">📜 금융상품 목록 📜</h2>
    
    <!-- 필터 섹션 -->
    <div class="bg-transparent mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- 상품 유형 선택 -->
        <div class="space-y-2">
          <label class="block text-sm font-bold text-gray-700">상품 유형</label>
          <select 
            v-model="selectedType"
            class="block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent font-bold"
          >
            <option value="deposit" class="font-bold">예금</option>
            <option value="saving" class="font-bold">적금</option>
          </select>
        </div>

        <!-- 은행 선택 -->
        <div class="space-y-2">
          <label class="block text-sm font-bold text-gray-700">은행</label>
          <select 
            v-model="selectedBank"
            class="block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent font-bold"
          >
            <option value="" class="font-bold">전체</option>
            <option v-for="bank in banks" :key="bank" :value="bank" class="font-bold">{{ bank }}</option>
          </select>
        </div>

        <!-- 예치 기간 선택 -->
        <div class="space-y-2">
          <label class="block text-sm font-bold text-gray-700">예치 기간</label>
          <select 
            v-model="selectedTerm"
            class="block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent font-bold"
          >
            <option value="" class="font-bold">전체</option>
            <option value="6" class="font-bold">6개월</option>
            <option value="12" class="font-bold">12개월</option>
            <option value="24" class="font-bold">24개월</option>
            <option value="36" class="font-bold">36개월</option>
          </select>
        </div>

        <!-- 검색 버튼 -->
        <div class="flex items-end">
          <button 
            @click="applyFilters"
            class="w-full px-4 py-2 bg-[#006775] text-white rounded-lg hover:bg-[#005761] transition-colors font-bold"
          >
            확인
          </button>
        </div>
      </div>
    </div>

    <!-- 로딩 표시 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#006775]"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="text-red-500 text-center py-12">
      {{ error }}
    </div>

    <!-- 상품 목록 (카드 형식) -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="(product, index) in filteredProducts" 
           :key="product.fin_prdt_cd" 
           class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <!-- 은행 로고 영역 -->
        <div class="h-40 bg-white flex items-center justify-center p-4">
          <div class="h-auto w-3/4 object-contain">
            <img
              :src="getBankLogo(product.kor_co_nm)"
              :alt="product.kor_co_nm + ' 로고'"
              class="h-full w-auto object-contain"
            >
          </div>
        </div>
        
        <!-- 상품 정보 -->
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <p class="text-sm text-gray-500 mb-1">{{ product.kor_co_nm }}</p>
              <router-link
                :to="selectedType === 'saving'
                  ? `/saving/${product.fin_prdt_nm}`
                  : `/deposit/${product.fin_prdt_nm}`"
                class="text-lg font-semibold text-gray-900 hover:text-[#006775]"
              >
                {{ product.fin_prdt_nm }}
              </router-link>
            </div>
            <button 
              @click="toggleInterest(product)"
              :class="[
                'p-2 text-2xl',
                product.is_interested ? 'text-yellow-500' : 'text-gray-300'
              ]"
            >
              ★
            </button>
          </div>

          <!-- 금리 정보 -->
          <div class="space-y-2">
            <div v-if="!selectedTerm || selectedTerm === '6'" class="flex justify-between">
              <span class="text-gray-600">6개월</span>
              <span class="font-semibold">{{ getInterestRate(product, 6) }}%</span>
            </div>
            <div v-if="!selectedTerm || selectedTerm === '12'" class="flex justify-between">
              <span class="text-gray-600">12개월</span>
              <span class="font-semibold">{{ getInterestRate(product, 12) }}%</span>
            </div>
            <div v-if="!selectedTerm || selectedTerm === '24'" class="flex justify-between">
              <span class="text-gray-600">24개월</span>
              <span class="font-semibold">{{ getInterestRate(product, 24) }}%</span>
            </div>
            <div v-if="!selectedTerm || selectedTerm === '36'" class="flex justify-between">
              <span class="text-gray-600">36개월</span>
              <span class="font-semibold">{{ getInterestRate(product, 36) }}%</span>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-100">
            <p class="text-sm text-gray-500">공시 제출일: {{ product.dcls_month }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

// 은행 로고 이미지 import
import 경남은행로고 from '@/assets/bank_img/경남은행.png'
import 광주은행로고 from '@/assets/bank_img/광주은행.png'
import 국민은행로고 from '@/assets/bank_img/국민은행.png'
import 농협은행로고 from '@/assets/bank_img/농협은행주식회사.png'
import 부산은행로고 from '@/assets/bank_img/부산은행.png'
import 수협은행로고 from '@/assets/bank_img/수협은행.png'
import 신한은행로고 from '@/assets/bank_img/신한은행.png'
import 아이엠뱅크로고 from '@/assets/bank_img/아이엠뱅크.png'
import 우리은행로고 from '@/assets/bank_img/우리은행.png'
import 전북은행로고 from '@/assets/bank_img/전북은행.png'
import 제주은행로고 from '@/assets/bank_img/제주은행.png'
import 카카오뱅크로고 from '@/assets/bank_img/주식회사 카카오뱅크.png'
import 케이뱅크로고 from '@/assets/bank_img/주식회사 케이뱅크.png'
import 기업은행로고 from '@/assets/bank_img/중소기업은행.png'
import 토스뱅크로고 from '@/assets/bank_img/토스뱅크 주식회사.png'
import 하나은행로고 from '@/assets/bank_img/하나은행.png'
import 산업은행로고 from '@/assets/bank_img/한국산업은행.png'
import SC은행로고 from '@/assets/bank_img/한국스탠다드차타드은행.png'

// 은행 로고 매핑
const bankLogoMap = {
  '경남은행': 경남은행로고,
  '광주은행': 광주은행로고,
  '국민은행': 국민은행로고,
  'KB국민은행': 국민은행로고,
  '농협은행주식회사': 농협은행로고,
  '부산은행': 부산은행로고,
  'BNK부산은행': 부산은행로고,
  '수협은행': 수협은행로고,
  '신한은행': 신한은행로고,
  '아이엠뱅크': 아이엠뱅크로고,
  '우리은행': 우리은행로고,
  '전북은행': 전북은행로고,
  '제주은행': 제주은행로고,
  '주식회사 카카오뱅크': 카카오뱅크로고,
  '카카오뱅크': 카카오뱅크로고,
  '주식회사 케이뱅크': 케이뱅크로고,
  '케이뱅크': 케이뱅크로고,
  '중소기업은행': 기업은행로고,
  'IBK기업은행': 기업은행로고,
  '토스뱅크 주식회사': 토스뱅크로고,
  '토스뱅크': 토스뱅크로고,
  '하나은행': 하나은행로고,
  '한국산업은행': 산업은행로고,
  '한국스탠다드차타드은행': SC은행로고,
  'SC제일은행': SC은행로고
}

// 은행 로고 가져오기 함수
const getBankLogo = (bankName) => {
  console.log('은행명:', bankName) // 디버깅을 위한 로그 추가
  return bankLogoMap[bankName] || ''
}

// 상태 관리
const selectedType = ref('deposit')
const selectedBank = ref('')
const selectedTerm = ref('')
const products = ref([])
const banks = ref([])
const loading = ref(false)
const error = ref(null)
const router = useRouter()

// API 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    Authorization: `Token ${localStorage.getItem('token')}`
  }
})

// 은행 목록 가져오기
const fetchBanks = async () => {
  try {
    const response = await api.get(`/${selectedType.value}/`)
    const uniqueBanks = [...new Set(response.data.map(product => product.kor_co_nm))]
    banks.value = uniqueBanks
  } catch (err) {
    console.error('은행 목록을 가져오는데 실패했습니다:', err)
  }
}

// 상품 목록 가져오기
const fetchProducts = async () => {
  loading.value = true
  error.value = null
  
  try {
    // 선택된 은행이 있는 경우
    if (selectedBank.value) {
      let url = `bank/${selectedType.value}/${selectedBank.value}/`
      if (selectedTerm.value) {
        url += `?term=${selectedTerm.value}`
      }
      const response = await api.get(url)
      const sampleProduct = response.data[0]
      console.log('Sample Product Full Data:', sampleProduct)
      console.log('Sample Product Keys:', Object.keys(sampleProduct))
      console.log('Sample Product Interest Data:', sampleProduct.interest || sampleProduct.intr_rate || sampleProduct.options)
      products.value = response.data
    } 
    // 전체 목록 조회
    else {
      const response = await api.get(`/${selectedType.value}/`)
      const sampleProduct = response.data[0]
      console.log('Sample Product Full Data:', sampleProduct)
      console.log('Sample Product Keys:', Object.keys(sampleProduct))
      console.log('Sample Product Interest Data:', sampleProduct.interest || sampleProduct.intr_rate || sampleProduct.options)
      products.value = response.data
    }
  } catch (err) {
    console.error('상품 목록을 가져오는데 실패했습니다:', err)
    error.value = '상품 정보를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 필터 적용
const applyFilters = async () => {
  await fetchProducts()
}

// 특정 기간의 이자율 가져오기
const getInterestRate = (product, term) => {
  console.log('Processing product for term:', term, product)
  
  // 옵션 데이터 가져오기
  const options = selectedType.value === 'deposit' 
    ? product.depositoption_set 
    : product.savingoption_set

  if (!options || !Array.isArray(options)) {
    console.log('No options found for product:', product.fin_prdt_nm)
    return '-'
  }

  // 해당 기간의 옵션 찾기
  const option = options.find(opt => Number(opt.save_trm) === Number(term))
  console.log('Found option for term:', term, option)

  if (!option) return '-'
  
  // 이자율 반환 (intr_rate2가 있다면 더 높은 우대금리 반환)
  return option.intr_rate2 && Number(option.intr_rate2) > Number(option.intr_rate)
    ? option.intr_rate2
    : option.intr_rate
}

// 관심 상품 토글
const toggleInterest = async (product) => {
  try {
    const response = await api.post(`/like/${selectedType.value}/${product.fin_prdt_cd}/`)
    product.is_interested = response.data.status === 'liked'
  } catch (err) {
    console.error('관심 상품 설정에 실패했습니다:', err)
    if (err.response?.status === 401) {
      // 로그인되지 않은 경우 로그인 페이지로 이동
      router.push('/login')
    }
  }
}

// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(async () => {
  await fetchBanks()
  await fetchProducts()
})

// 상품 타입이나 은행 선택이 변경될 때 목록 갱신
watch([selectedType, selectedBank], () => {
  fetchProducts()
})

const filteredProducts = computed(() => {
  // 예치 기간이 선택되지 않았으면 전체 반환
  if (!selectedTerm.value) return products.value;

  // 예치 기간이 선택된 경우, 해당 기간의 금리가 실제로 존재하는 상품만 반환
  return products.value.filter(product => {
    const rate = getInterestRate(product, selectedTerm.value);
    return rate !== '-';
  });
});
</script> 
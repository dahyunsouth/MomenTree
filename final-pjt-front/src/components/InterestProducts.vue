<template>
  <div class="interest-products p-6 bg-white/30 rounded-3xl shadow-lg">
    <h2 class="text-2xl font-bold mb-6">⭐관심 상품 목록⭐</h2>
    
    <!-- 상품 유형 선택 -->
    <div class="mb-8">
      <div class="inline-flex p-1 space-x-1 bg-white/40 rounded-xl shadow-sm">
        <button 
          @click="selectedType = 'deposit'"
          :class="[
            'px-6 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200',
            selectedType === 'deposit' 
              ? 'bg-[#006775] text-white shadow-md transform scale-105' 
              : 'bg-transparent text-gray-600 hover:bg-white/50'
          ]"
        >
          예금
        </button>
        <button 
          @click="selectedType = 'saving'"
          :class="[
            'px-6 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200',
            selectedType === 'saving' 
              ? 'bg-[#006775] text-white shadow-md transform scale-105' 
              : 'bg-transparent text-gray-600 hover:bg-white/50'
          ]"
        >
          적금
        </button>
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

    <!-- 상품이 없을 때 -->
    <div v-else-if="!products.length" class="text-gray-500 text-center py-12">
      관심 등록된 {{ selectedType === 'deposit' ? '예금' : '적금' }} 상품이 없습니다.
    </div>

    <!-- 상품 목록 -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200 rounded-2xl overflow-hidden">
        <thead class="bg-gray-50/80">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">금융회사</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상품명</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">6개월</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">12개월</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">24개월</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">36개월</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">관심상품</th>
          </tr>
        </thead>
        <tbody class="bg-white/80 divide-y divide-gray-200">
          <tr v-for="product in products" :key="product.fin_prdt_cd" class="hover:bg-gray-50/90 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ product.kor_co_nm }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ product.fin_prdt_nm }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ getInterestRate(product, 6) }}%</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ getInterestRate(product, 12) }}%</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ getInterestRate(product, 24) }}%</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ getInterestRate(product, 36) }}%</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <button 
                @click="toggleInterest(product)"
                class="p-2 rounded-full transition-colors text-yellow-500 hover:text-yellow-600"
              >
                ★
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const emit = defineEmits(['update'])

// 상태 관리
const selectedType = ref('deposit')
const products = ref([])
const loading = ref(false)
const error = ref(null)

// API 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    Authorization: `Token ${localStorage.getItem('token')}`
  }
})

// 관심 상품 목록 가져오기
const fetchProducts = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get(`/interest/${selectedType.value}/`)
    products.value = response.data
  } catch (err) {
    console.error('관심 상품 목록을 가져오는데 실패했습니다:', err)
    error.value = '관심 상품 정보를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 특정 기간의 이자율 가져오기
const getInterestRate = (product, term) => {
  const options = selectedType.value === 'deposit' 
    ? product.depositoption_set 
    : product.savingoption_set

  if (!options || !Array.isArray(options)) {
    return '-'
  }

  const option = options.find(opt => Number(opt.save_trm) === Number(term))
  if (!option) return '-'
  
  return option.intr_rate2 && Number(option.intr_rate2) > Number(option.intr_rate)
    ? option.intr_rate2
    : option.intr_rate
}

// 관심 상품 토글
const toggleInterest = async (product) => {
  try {
    await api.post(`/like/${selectedType.value}/${product.fin_prdt_cd}/`)
    // 목록 새로고침
    fetchProducts()
  } catch (err) {
    console.error('관심 상품 설정에 실패했습니다:', err)
  }
}

// 관심상품 변경 시 부모에 알림
const emitUpdate = () => {
  emit('update', products.value)
}

watch(products, emitUpdate, { deep: true })
onMounted(emitUpdate)

// 상품 타입이 변경될 때 목록 갱신
watch(selectedType, fetchProducts)
</script> 
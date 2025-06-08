<template>
  <div v-if="saving">
    <!-- 상품 기본 정보 + 가입 정보 + 금리/옵션 정보 카드 -->
    <div class="bg-white/60 rounded-xl shadow-lg p-12 mb-6 border-2 border-gray-200">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
        <div>
          <h2 class="text-2xl font-bold text-blue-900 mb-1">{{ saving.fin_prdt_nm }}</h2>
          <p class="text-lg text-gray-700 mb-2">{{ saving.kor_co_nm }}</p>
        </div>
        <div class="text-sm text-gray-500 mt-2 md:mt-0">
          <span class="mr-4"><b>공시 제출월:</b> {{ saving.dcls_month }}</span>
          <span><b>상품 코드:</b> {{ saving.fin_prdt_cd }}</span>
        </div>
      </div>
      <div class="mb-6">
        <h3 class="font-semibold mb-2 text-blue-800">가입 정보</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2 text-gray-800">
          <div><b>가입 방법:</b> {{ saving.join_way }}</div>
          <div><b>가입 대상:</b> {{ saving.join_member }}</div>
          <div><b>가입 제한:</b> {{ saving.join_deny === 0 ? '제한 없음' : '제한 있음' }}</div>
          <div><b>최고 한도:</b> {{ saving.max_limit ? saving.max_limit + '원' : '제한 없음' }}</div>
          <div class="md:col-span-2"><b>기타 유의사항:</b> {{ saving.etc_note }}</div>
        </div>
      </div>
      <!-- 금리/옵션 정보 -->
      <div>
        <h3 class="font-semibold mb-3 text-blue-800">금리/옵션 정보</h3>
        <div class="flex gap-4 mb-4">
          <div>
            <label class="font-semibold mr-2">저축기간</label>
            <select v-model="selectedTerm" class="border rounded px-2 py-1">
              <option value="">전체</option>
              <option v-for="term in termOptions" :key="term" :value="term">{{ term }}개월</option>
            </select>
          </div>
          <div>
            <label class="font-semibold mr-2">금리유형</label>
            <select v-model="selectedRateType" class="border rounded px-2 py-1">
              <option value="">전체</option>
              <option v-for="type in rateTypeOptions" :key="type" :value="type">{{ type }}</option>
            </select>
          </div>
        </div>
        <table class="min-w-full border text-sm">
          <thead>
            <tr class="bg-gray-100">
              <th class="border px-2 py-1">저축기간</th>
              <th class="border px-2 py-1">금리유형</th>
              <th class="border px-2 py-1">적립유형</th>
              <th class="border px-2 py-1">기본금리</th>
              <th class="border px-2 py-1">최고우대금리</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="option in sortedOptions" :key="option.id">
              <td class="border px-2 py-1">{{ option.save_trm }}개월</td>
              <td class="border px-2 py-1">{{ option.intr_rate_type_nm }}</td>
              <td class="border px-2 py-1">{{ option.rsrv_type_nm }}</td>
              <td class="border px-2 py-1">{{ option.intr_rate ? option.intr_rate + '%' : '-' }}</td>
              <td class="border px-2 py-1">{{ option.intr_rate2 ? option.intr_rate2 + '%' : '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 만기 후 이자율/특별 조건 카드 -->
    <div class="text-xs">
      <div class="mb-1"><span class="font-semibold">만기 후 이자율:</span> {{ saving.mtrt_int }}</div>
      <div><span class="font-semibold">특별 조건:</span> {{ saving.spcl_cnd }}</div>
    </div>
  </div>
  <div v-else>로딩 중...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const props = defineProps({
  saving_name: {
    type: String,
    required: true
  }
})

const route = useRoute()
const saving = ref(null)
const selectedTerm = ref('')
const selectedRateType = ref('')

onMounted(async () => {
  console.log('SavingDetail onMounted 실행');
  console.log('saving_name:', props.saving_name)
  try {
    const res = await axios.get(
      `http://localhost:8000/api/saving/${encodeURIComponent(props.saving_name)}/`,
      { headers: { Authorization: `Token ${localStorage.getItem('token')}` } }
    )
    saving.value = res.data
    console.log('saving:', saving.value)
  } catch (e) {
    console.error('상세 정보 불러오기 실패:', e)
  }
})

// 드롭다운 옵션 목록
const termOptions = computed(() => {
  if (!saving.value || !saving.value.savingoption_set) return []
  const terms = saving.value.savingoption_set.map(opt => opt.save_trm)
  return [...new Set(terms)].sort((a, b) => a - b)
})
const rateTypeOptions = computed(() => {
  if (!saving.value || !saving.value.savingoption_set) return []
  const types = saving.value.savingoption_set.map(opt => opt.intr_rate_type_nm)
  return [...new Set(types)]
})

// 정렬 및 필터링된 옵션 computed
const sortedOptions = computed(() => {
  if (!saving.value || !saving.value.savingoption_set) return []
  let opts = [...saving.value.savingoption_set]
  if (selectedTerm.value) {
    opts = opts.filter(opt => String(opt.save_trm) === String(selectedTerm.value))
  }
  if (selectedRateType.value) {
    opts = opts.filter(opt => opt.intr_rate_type_nm === selectedRateType.value)
  }
  return opts.sort((a, b) => {
    if (a.save_trm !== b.save_trm) return a.save_trm - b.save_trm
    if (a.rsrv_type_nm !== b.rsrv_type_nm) return a.rsrv_type_nm.localeCompare(b.rsrv_type_nm)
    return a.intr_rate_type_nm.localeCompare(b.intr_rate_type_nm)
  })
})
</script>

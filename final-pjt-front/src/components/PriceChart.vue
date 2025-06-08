<template>
  <div class="relative min-h-[500px]">
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#006775]"></div>
    </div>
    <div v-if="error" class="flex items-center justify-center h-[400px] text-gray-500">
      {{ error }}
    </div>
    <canvas v-else ref="chartRef" style="min-height: 500px;"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

// axios 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:8000'
})

const props = defineProps({
  asset: {
    type: String,
    required: true
  },
  startDate: {
    type: String,
    required: true
  },
  endDate: {
    type: String,
    required: true
  }
})

const chartRef = ref(null)
const loading = ref(false)
const error = ref('')
let chart = null

const validateDates = () => {
  if (!props.startDate || !props.endDate) {
    error.value = '시작일과 종료일을 모두 선택해주세요.'
    return false
  }

  const start = new Date(props.startDate)
  const end = new Date(props.endDate)

  if (end < start) {
    error.value = '선택된 조건에 해당하는 데이터가 없습니다.'
    return false
  }

  error.value = ''
  return true
}

const fetchData = async () => {
  if (!validateDates()) {
    if (chart) {
      chart.destroy()
      chart = null
    }
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    console.log('Fetching data with params:', {
      asset: props.asset.toUpperCase(),
      start_date: props.startDate,
      end_date: props.endDate
    })

    const response = await api.get('/golds/api/prices/', {
      params: {
        asset: props.asset.toUpperCase(),
        start_date: props.startDate,
        end_date: props.endDate
      }
    })

    console.log('API Response:', response.data)

    if (!response.data || !response.data.labels || response.data.labels.length === 0) {
      error.value = '선택된 조건에 해당하는 데이터가 없습니다.'
      if (chart) {
        chart.destroy()
        chart = null
      }
      return
    }

    if (chart) {
      chart.destroy()
    }

    const ctx = chartRef.value.getContext('2d')
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: response.data.labels,
        datasets: [{
          label: `${props.asset.toUpperCase()} 가격`,
          data: response.data.datasets[0].data,
          borderColor: props.asset === 'gold' ? '#FFD700' : '#C0C0C0',
          backgroundColor: 'rgba(0, 0, 0, 0)',  // 투명 배경
          borderWidth: 2,
          tension: 0.1,
          fill: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: `${props.asset.toUpperCase()} 가격 추이`
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            grace: '0%',  // 자동 여백 제거
            ticks: {
              stepSize: props.asset === 'gold' ? 10 : 0.5,
              callback: function(value) {
                return value.toLocaleString() + ' USD'
              }
            },
            grid: {
              display: true,
              drawBorder: true,
              color: 'rgba(0, 0, 0, 0.1)'
            },
            // y축 범위를 더 넓게 설정
            afterDataLimits: (scale) => {
              const dataMin = Math.min(...scale.chart.data.datasets[0].data);
              const dataMax = Math.max(...scale.chart.data.datasets[0].data);
              const range = dataMax - dataMin;
              
              // 더 넓은 범위로 설정 (위아래 20%)
              scale.min = dataMin - (range * 0.2);
              scale.max = dataMax + (range * 0.2);
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              maxRotation: 45,
              minRotation: 45
            }
          }
        }
      }
    })
  } catch (err) {
    console.error('차트 데이터를 불러오는데 실패했습니다:', err)
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

watch([() => props.asset, () => props.startDate, () => props.endDate], fetchData)

onMounted(fetchData)
</script> 
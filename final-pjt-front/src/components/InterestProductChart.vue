<template>
  <div style="background: rgba(255, 255, 255, 0.3); border-radius: 16px; padding: 2rem;">
    <h2 class="text-2xl font-bold mb-6">⭐관심 상품 금리 비교⭐</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart, BarElement, CategoryScale, LinearScale, Legend, Tooltip } from 'chart.js'

Chart.register(BarElement, CategoryScale, LinearScale, Legend, Tooltip)

const props = defineProps({
  products: Array // [{ name, intr_rate, intr_rate2 }]
})

// 평균 계산
const avgBase = computed(() => {
  const arr = props.products.map(p => Number(p.intr_rate) || 0)
  if (!arr.length) return 0
  return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2)
})
const avgPrefer = computed(() => {
  const arr = props.products.map(p => Number(p.intr_rate2) || 0)
  if (!arr.length) return 0
  return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2)
})

// x축 라벨: 평균 금리 + 각 상품명
const labels = computed(() => ['평균 금리', ...props.products.map(p => p.name)])

// 저축 금리 데이터: [평균, 상품1, 상품2, ...]
const baseRates = computed(() => [Number(avgBase.value), ...props.products.map(p => Number(p.intr_rate) || 0)])
// 최고 우대금리 데이터: [평균, 상품1, 상품2, ...]
const preferRates = computed(() => [Number(avgPrefer.value), ...props.products.map(p => Number(p.intr_rate2) || 0)])

const chartData = computed(() => ({
  labels: labels.value,
  datasets: [
    {
      label: '저축 금리',
      backgroundColor: '#4bc0c0',
      data: baseRates.value
    },
    {
      label: '최고 우대금리',
      backgroundColor: '#7ed957',
      data: preferRates.value
    }
  ]
}))

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: '#222',
        font: { size: 16 }
      },
      grid: {
        color: '#e0e0e0'
      }
    },
    x: {
      ticks: {
        color: '#222',
        font: { size: 16 }
      },
      grid: {
        color: '#e0e0e0'
      }
    }
  }
}
</script> 
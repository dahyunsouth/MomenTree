<template>
  <div class="p-6 bg-white/30 rounded-3xl shadow-lg">
    <h2 class="text-2xl font-bold mb-6">🪙 현물 상품 비교 🪙</h2>
    
    <!-- 필터 섹션 -->
    <div class="mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 날짜 선택 -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">시작일:</label>
          <input 
            type="date" 
            v-model="startDate"
            class="block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
          >
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">종료일:</label>
          <input 
            type="date" 
            v-model="endDate"
            class="block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
          >
        </div>
      </div>

      <!-- 자산 선택 버튼 -->
      <div class="flex gap-4 mt-6">
        <button 
          @click="selectedAsset = 'gold'"
          :class="[
            'flex-1 py-2 px-4 rounded-lg font-medium transition-colors',
            selectedAsset === 'gold' 
              ? 'bg-[#FFD700] text-gray-900 border-2 border-[#B8860B]' 
              : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
          ]"
        >
          <span class="font-bold">금(Gold)</span>
        </button>
        <button 
          @click="selectedAsset = 'silver'"
          :class="[
            'flex-1 py-2 px-4 rounded-lg font-medium transition-colors',
            selectedAsset === 'silver' 
              ? 'bg-[#C0C0C0] text-gray-900 border-2 border-[#808080]' 
              : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
          ]"
        >
          <span class="font-bold">은(Silver)</span>
        </button>
      </div>
    </div>

    <!-- 차트 영역 -->
    <div class="bg-white/50 rounded-2xl p-4 min-h-[400px]">
      <PriceChart 
        :asset="selectedAsset"
        :startDate="startDate"
        :endDate="endDate"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PriceChart from './PriceChart.vue'

const startDate = ref('')
const endDate = ref('')
const selectedAsset = ref('gold')
</script> 
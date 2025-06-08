<template>
  <div class="flex justify-center items-center gap-2 mt-6">
    <button 
      @click="$emit('page-change', currentPage - 1)"
      :disabled="currentPage === 1"
      class="px-3 py-2 rounded hover:bg-gray-100 disabled:opacity-50"
    >
      &lt;
    </button>
    
    <template v-for="page in visiblePages" :key="page">
      <button 
        v-if="page !== '...'"
        @click="$emit('page-change', page)"
        :class="[
          'px-3 py-2 rounded',
          currentPage === page ? 'bg-[#006775] text-white' : 'hover:bg-gray-100'
        ]"
      >
        {{ page }}
      </button>
      <span v-else class="px-2">{{ page }}</span>
    </template>

    <button 
      @click="$emit('page-change', currentPage + 1)"
      :disabled="currentPage === totalPages"
      class="px-3 py-2 rounded hover:bg-gray-100 disabled:opacity-50"
    >
      &gt;
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
})

defineEmits(['page-change'])

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 4 // 시작, 끝 페이지 제외하고 보여줄 최대 페이지 수

  // 항상 첫 페이지 추가
  pages.push(1)

  let start = Math.max(2, props.currentPage - 1)
  let end = Math.min(start + maxVisible - 1, props.totalPages - 1)

  // 시작 페이지가 2보다 크면 ... 추가
  if (start > 2) {
    pages.push('...')
  }

  // 중간 페이지들 추가
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  // 마지막 페이지 전에 ... 추가
  if (end < props.totalPages - 1) {
    pages.push('...')
  }

  // 마지막 페이지가 아직 추가되지 않았다면 추가
  if (props.totalPages > 1) {
    pages.push(props.totalPages)
  }

  return pages
})
</script> 
<template>
  <div class="p-6 bg-white/30 rounded-3xl shadow-lg">
    <h2 class="text-2xl font-bold mb-6">🔍 관심 종목 정보 검색 🔍</h2>
    
    <!-- 검색 섹션 -->
    <div class="flex gap-4">
      <input 
        v-model="searchQuery"
        type="text"
        placeholder="검색어를 입력하세요"
        class="flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
        @keyup.enter="searchVideos"
      />
      <button 
        @click="searchVideos"
        class="bg-[#006775] hover:bg-[#005865] text-white px-6 py-2 rounded-lg transition-colors"
      >
        검색
      </button>
    </div>
    

    <!-- 로딩 표시 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#006775]"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="text-red-500 text-center py-12">
      {{ error }}
    </div>

    <!-- 검색 결과 -->
    <div v-else-if="videos.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="video in videos" 
        :key="video.id.videoId"
        class="bg-white rounded-lg overflow-hidden shadow hover:shadow-lg transition-shadow cursor-pointer"
        @click="goToVideoDetail(video.id.videoId)"
      >
        <img 
          :src="video.snippet.thumbnails.medium.url" 
          :alt="video.snippet.title"
          class="w-full h-48 object-cover"
        />
        <div class="p-4">
          <h3 class="text-lg font-semibold mb-2 line-clamp-2">{{ video.snippet.title }}</h3>
          <p class="text-sm text-gray-600">{{ formatDate(video.snippet.publishedAt) }}</p>
        </div>
      </div>
    </div>

    <!-- 검색 결과 없음 -->
    <div v-else-if="!loading && searchQuery" class="text-center py-12 text-gray-600">
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const searchQuery = ref('')
const videos = ref([])
const loading = ref(false)
const error = ref(null)

// YouTube API 키를 환경 변수에서 가져옵니다
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const searchVideos = async () => {
  if (!searchQuery.value.trim()) return

  loading.value = true
  error.value = null
  videos.value = []

  if (!API_KEY) {
    error.value = 'YouTube API 키가 설정되지 않았습니다. 환경 설정을 확인해주세요.'
    loading.value = false
    return
  }

  try {
    const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
      params: {
        part: 'snippet',
        maxResults: 15,
        q: searchQuery.value + ' 주식 투자',
        type: 'video',
        key: API_KEY
      }
    })

    if (response.data.items && response.data.items.length > 0) {
      videos.value = response.data.items
    } else {
      error.value = '검색 결과가 없습니다.'
    }
  } catch (err) {
    if (err.response && err.response.status === 400) {
      error.value = 'API 키가 유효하지 않습니다. 환경 설정을 확인해주세요.'
    } else {
      error.value = '검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
    }
    console.error('YouTube API 오류:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const goToVideoDetail = (videoId) => {
  router.push(`/search/${videoId}`)
}
</script> 
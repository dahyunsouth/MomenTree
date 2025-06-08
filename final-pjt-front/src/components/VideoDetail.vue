<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- 메인 비디오 컨텐츠 (2/3 너비) -->
    <div class="lg:col-span-2 p-6 bg-white rounded-3xl shadow-lg">
      <!-- 로딩 표시 -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#006775]"></div>
      </div>

      <!-- 에러 메시지 -->
      <div v-else-if="error" class="text-red-500 text-center py-12">
        {{ error }}
      </div>

      <!-- 비디오 상세 정보 -->
      <div v-else-if="video" class="space-y-6">
        <!-- 뒤로 가기 버튼 -->
        <button 
          @click="router.back()"
          class="flex items-center gap-2 px-6 py-2.5 bg-transparent hover:bg-[#006775] text-[#006775] hover:text-white font-bold rounded-full border-2 border-[#006775] transition-all duration-200 mb-6"
        >
          <span class="text-lg">←</span>
          <span>목록으로 돌아가기</span>
        </button>

        <!-- 비디오 플레이어 -->
        <div class="aspect-w-16 aspect-h-9 bg-black rounded-lg overflow-hidden">
          <iframe
            :src="'https://www.youtube.com/embed/' + videoId"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            class="w-full h-full"
          ></iframe>
        </div>

        <!-- 비디오 정보 -->
        <div class="space-y-4">
          <h1 class="text-2xl font-bold">{{ video.snippet.title }}</h1>
          
          <!-- 채널 정보 및 통계 -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-4 border-b border-gray-200">
            <div class="flex items-center gap-4">
              <div class="font-medium">{{ video.snippet.channelTitle }}</div>
              <div class="text-sm text-gray-600">{{ formatDate(video.snippet.publishedAt) }}</div>
            </div>
            
            <div class="video-stats">
              <span v-if="video.statistics">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z" />
                  <path fill-rule="evenodd" d="M.664 10.59a1.651 1.651 0 010-1.186A10.004 10.004 0 0110 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0110 17c-4.257 0-7.893-2.66-9.336-6.41zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                </svg>
                {{ formatNumber(video.statistics.viewCount) }}회
              </span>
              <span v-if="video.statistics">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                </svg>
                {{ formatNumber(video.statistics.likeCount) }}
              </span>
            </div>
          </div>

          <!-- 비디오 설명 -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="font-medium mb-2">설명</h3>
            <p class="text-gray-700 whitespace-pre-line">{{ video.snippet.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 영상 요약 카드 (1/3 너비) -->
    <div class="lg:col-span-1 p-6 bg-white rounded-3xl shadow-lg h-fit sticky top-6">
      <h2 class="text-xl font-bold mb-6 text-gray-800">🎬 영상 요약 🎬</h2>
      
      <button 
        @click="summarizeVideo" 
        class="w-full bg-[#006775] hover:bg-[#005766] text-white font-bold py-3 px-4 rounded-lg transition-colors mb-4"
        :disabled="isSummarizing"
      >
        {{ isSummarizing ? '요약 중...' : '영상 요약하기' }}
      </button>
      
      <div v-if="summary" class="mt-4 p-4 bg-gray-50 rounded-lg">
        <p class="whitespace-pre-line text-gray-700">{{ summary }}</p>
      </div>
      
      <div v-if="summaryError" class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
        {{ summaryError }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const videoId = route.params.id
const video = ref(null)
const loading = ref(true)
const error = ref(null)
const summary = ref('')
const summaryError = ref('')
const isSummarizing = ref(false)

// YouTube API 키를 환경 변수에서 가져옵니다
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const fetchVideoDetails = async () => {
  if (!videoId) {
    error.value = '비디오 ID가 유효하지 않습니다.'
    loading.value = false
    return
  }

  if (!API_KEY) {
    error.value = 'YouTube API 키가 설정되지 않았습니다. 환경 설정을 확인해주세요.'
    loading.value = false
    return
  }

  try {
    const response = await axios.get('https://www.googleapis.com/youtube/v3/videos', {
      params: {
        part: 'snippet,statistics',
        id: videoId,
        key: API_KEY
      }
    })

    if (response.data.items && response.data.items.length > 0) {
      video.value = response.data.items[0]
    } else {
      error.value = '비디오를 찾을 수 없습니다.'
    }
  } catch (err) {
    if (err.response && err.response.status === 400) {
      error.value = 'API 키가 유효하지 않습니다. 환경 설정을 확인해주세요.'
    } else {
      error.value = '비디오 정보를 불러오는 중 오류가 발생했습니다.'
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

const formatNumber = (num) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

const summarizeVideo = async () => {
  try {
    isSummarizing.value = true
    summaryError.value = ''
    
    console.log('요약 시작 - 비디오 ID:', videoId)
    const response = await axios.post('http://localhost:8000/videos/summarize/', {
      video_url: `https://www.youtube.com/watch?v=${videoId}`
    })
    
    console.log('요약 응답:', response.data)
    summary.value = response.data.summary
  } catch (error) {
    console.error('영상 요약 중 상세 에러:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      url: error.config?.url,
      data: error.config?.data
    })
    summaryError.value = '영상을 요약하는 중에 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
  } finally {
    isSummarizing.value = false
  }
}

onMounted(() => {
  fetchVideoDetails()
})
</script>

<style>
.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
}

.aspect-w-16 iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.video-stats {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.video-stats span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style> 



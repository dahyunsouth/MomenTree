<template>
  <div class="container py-4">
    <button class="btn btn-link mb-3" @click="$router.back()">
      ← 뒤로가기
    </button>
    <div v-if="video" class="video-detail">
      <h2 class="mb-3">{{ video.snippet.title }}</h2>
      <p class="text-muted mb-4">
        업로드 날짜: {{ formatDate(video.snippet.publishedAt) }}
      </p>
      <div class="ratio ratio-16x9 mb-4">
        <iframe
          :src="`https://www.youtube.com/embed/${video.id}`"
          title="YouTube video player"
          allowfullscreen
        ></iframe>
      </div>
      <p v-html="video.snippet.description"></p>
    </div>
    <div v-else class="text-center text-muted">
      로딩 중…
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VideoDetail',
  data() {
    return {
      video: null,
      apiKey: import.meta.env.VITE_YOUTUBE_API_KEY
    }
  },
  async created() {
    try {
      const id = this.$route.params.id
      const response = await axios({
        method: 'GET',
        url: 'https://www.googleapis.com/youtube/v3/videos',
        params: {
          key: this.apiKey,
          part: 'snippet,statistics',
          id: id
        }
      })

      if (response.data.items && response.data.items.length > 0) {
        this.video = response.data.items[0]
      } else {
        console.error('Video not found')
      }
    } catch (error) {
      console.error('Error fetching video:', error.response?.data || error.message)
    }
  },
  methods: {
    formatDate(value) {
      return new Date(value).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.video-detail h2 {
  word-break: keep-all;
}
.video-detail p {
  white-space: pre-wrap;
}
</style>

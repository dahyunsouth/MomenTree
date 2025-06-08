<template>
  <div class="container py-4">
    <button class="btn btn-link mb-3" @click="$router.back()">
      ← 뒤로가기
    </button>
    <h2 class="mb-4 text-center">비디오 검색</h2>
    <form @submit.prevent="searchVideos" class="input-group mb-4">
      <input
        v-model="query"
        type="text"
        class="form-control"
        placeholder="검색어를 입력하세요"
      />
      <button class="btn btn-success" type="submit">찾기</button>
    </form>

    <!-- 검색 결과 그리드 -->
    <div class="row g-4">
      <div
        v-for="video in videos"
        :key="video.id.videoId"
        class="col-sm-6 col-md-4"
      >
        <router-link
          :to="`/video/${video.id.videoId}`"
          class="text-decoration-none d-block h-100"
        >
          <div class="card h-100 video-card">
            <img
              :src="video.snippet.thumbnails.medium.url"
              class="card-img-top"
              :alt="video.snippet.title"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title small text-dark">
                {{ video.snippet.title }}
              </h5>
              <p class="card-text text-muted mt-auto">
                {{ new Date(video.snippet.publishedAt).toLocaleDateString() }}
              </p>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- 검색 후 결과 없을 때 -->
    <div
      v-if="searched && videos.length === 0"
      class="text-center mt-5 text-muted"
    >
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VideoSearch',
  data() {
    return {
      query: '',
      videos: [],
      searched: false,
      apiKey: import.meta.env.VITE_YOUTUBE_API_KEY
    }
  },
  created() {
    if (!this.apiKey) {
      console.error('YouTube API key is missing')
    }
  },
  methods: {
    async searchVideos() {
      this.searched = false

      if (!this.query.trim()) {
        this.videos = []
        this.searched = true
        return
      }

      const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY
      console.log('Search query:', this.query)

      try {
        const response = await axios({
          method: 'GET',
          url: 'https://www.googleapis.com/youtube/v3/search',
          params: {
            part: 'snippet',
            maxResults: 12,
            q: this.query,
            key: apiKey,
            type: 'video',
            regionCode: 'KR',
            safeSearch: 'none',
            videoEmbeddable: true
          },
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        })

        console.log('API Response:', response.data)

        if (response.data && response.data.items) {
          this.videos = response.data.items
        } else {
          console.warn('No items in response:', response.data)
          this.videos = []
        }
      } catch (error) {
        console.error('YouTube API 오류:', {
          message: error.message,
          response: error.response?.data,
          config: {
            url: error.config?.url,
            params: error.config?.params,
            headers: error.config?.headers
          }
        })
        this.videos = []
      } finally {
        this.searched = true
      }
    }
  }
}
</script>

<style scoped>
.video-card {
  cursor: pointer;
  transition: transform .2s;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card-img-top {
  object-fit: cover;
  height: 180px;
}

.card-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

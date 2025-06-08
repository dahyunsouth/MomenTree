<template>
  <div class="p-8 bg-white/30 rounded-3xl shadow-lg max-w-2xl mx-auto mt-10">
    <h2 class="text-2xl font-bold mb-8 text-gray-800">✏️ 게시글 수정</h2>
    <div v-if="loading" class="text-center text-gray-500">로딩 중...</div>
    <div v-else class="space-y-6">
      <!-- 제목 입력 -->
      <div>
        <label class="block text-gray-700 font-bold mb-2">제목</label>
        <input 
          v-model="post.title" 
          placeholder="제목을 입력해주세요" 
          class="border border-gray-300 rounded-lg px-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-[#006775] focus:border-transparent transition-all"
        />
      </div>

      <!-- 내용 입력 -->
      <div>
        <label class="block text-gray-700 font-bold mb-2">내용</label>
        <textarea 
          v-model="post.content" 
          placeholder="내용을 입력해주세요" 
          class="border border-gray-300 rounded-lg px-4 py-3 w-full h-48 resize-none focus:outline-none focus:ring-2 focus:ring-[#006775] focus:border-transparent transition-all"
        ></textarea>
      </div>

      <!-- 버튼 영역 -->
      <div class="flex justify-end space-x-4 pt-4">
        <button 
          @click="updatePost" 
          class="bg-[#006775] text-white px-6 py-2 rounded-lg hover:bg-white hover:text-[#006775] border-2 border-[#006775] transition-colors font-bold"
        >
          수정 완료
        </button>
        <button 
          @click="cancelEdit" 
          class="bg-gray-400 text-white px-6 py-2 rounded-lg hover:bg-white hover:text-gray-600 border-2 border-gray-400 transition-colors font-bold"
        >
          취소
        </button>
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
const post = ref({ title: '', content: '' })
const loading = ref(true)
const postId = route.params.id

const fetchPostDetail = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/articles/${postId}/`)
    post.value = {
      title: res.data.title,
      content: res.data.content
    }
    loading.value = false
  } catch (e) {
    alert('게시글 정보를 불러오는데 실패했습니다.')
    router.push('/community')
  }
}

const updatePost = async () => {
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('title', post.value.title)
    formData.append('content', post.value.content)

    await axios.put(`http://localhost:8000/articles/${postId}/`, formData, {
      headers: {
        Authorization: `Token ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    alert('게시글이 성공적으로 수정되었습니다!')
    router.push(`/community/${postId}`)
  } catch (e) {
    alert('게시글 수정 실패(권한 필요)')
    console.error(e)
  }
}

const cancelEdit = () => {
  router.push(`/community/${postId}`)
}

onMounted(() => {
  fetchPostDetail()
})
</script>

<style scoped>
textarea {
  font-family: inherit;
}
</style> 
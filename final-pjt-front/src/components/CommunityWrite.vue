<template>
  <div class="p-8 bg-white/55 rounded-3xl shadow-lg max-w-2xl mx-auto mt-10">
    <h2 class="text-2xl font-bold mb-8 text-gray-800">✏️ 게시글 작성</h2>
    
    <div class="space-y-6">
      <!-- 제목 입력 -->
      <div>
        <label class="block text-gray-700 font-bold mb-2">제목</label>
        <input 
          v-model="title" 
          placeholder="제목을 입력해주세요" 
          class="border border-gray-300 rounded-lg px-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-[#006775] focus:border-transparent transition-all"
        />
      </div>

      <!-- 내용 입력 -->
      <div>
        <label class="block text-gray-700 font-bold mb-2">내용</label>
        <textarea 
          v-model="content" 
          placeholder="내용을 입력해주세요" 
          class="border border-gray-300 rounded-lg px-4 py-3 w-full h-48 resize-none focus:outline-none focus:ring-2 focus:ring-[#006775] focus:border-transparent transition-all"
        ></textarea>
      </div>

      <!-- 버튼 영역 -->
      <div class="flex justify-end pt-4">
        <button 
          @click="createPost" 
          class="bg-[#006775] text-white px-6 py-2 rounded-lg hover:bg-white hover:text-[#006775] border-2 border-[#006775] transition-colors font-bold"
        >
          작성하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const title = ref('')
const content = ref('')
const router = useRouter()

const createPost = async () => {
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('title', title.value)
    formData.append('content', content.value)

    await axios.post('http://localhost:8000/articles/', formData, {
      headers: {
        Authorization: `Token ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    alert('게시글이 작성되었습니다!')
    router.push('/community')
  } catch (e) {
    alert('게시글 작성 실패(로그인 필요)')
    console.error(e)
  }
}
</script>

<style scoped>
textarea {
  font-family: inherit;
}
</style> 
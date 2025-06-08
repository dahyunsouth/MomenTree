<template>
  <div class="p-6 bg-white/30 rounded-3xl shadow-lg">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">⁉️ 커뮤니티</h2>
      <button @click="goToWrite" class="bg-[#006775] text-white px-6 py-2 rounded-lg hover:bg-white hover:text-[#006775] border-2 border-[#006775] transition-colors font-bold">
        글 작성하기
      </button>
    </div>
    <div class="overflow-x-auto">
      <table class="min-w-full">
        <thead>
          <tr class="border-b">
            <th class="py-4 px-4 text-left text-gray-500 w-16">No.</th>
            <th class="py-4 px-4 text-left text-gray-500">Title</th>
            <th class="py-4 px-4 text-left text-gray-500 w-36">Nickname</th>
            <th class="py-4 px-4 text-left text-gray-500 w-36">Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.articleId" class="border-b hover:bg-gray-50 cursor-pointer" @click="goToDetail(post.articleId)">
            <td class="py-6 px-4 font-bold">{{ post.no }}</td>
            <td class="py-6 px-4 font-bold">
              {{ post.title }}
            </td>
            <td class="py-6 px-4 flex items-center">
              <img v-if="post.profile_image" :src="`http://localhost:8000${post.profile_image}`" class="w-8 h-8 rounded-full mr-2" />
              <span class="font-bold">{{ post.nickname }}</span>
            </td>
            <td class="py-6 px-4 font-bold">{{ post.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <Pagination 
      :currentPage="currentPage" 
      :totalPages="totalPages" 
      @page-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Pagination from './Pagination.vue'

const router = useRouter()
const currentPage = ref(1)
const totalPages = ref(1)
const posts = ref([])

const fetchPosts = async () => {
  try {
    const res = await axios.get('http://localhost:8000/articles/')
    posts.value = res.data.map((item, idx) => ({
      no: idx + 1,
      articleId: item.id,
      title: item.title,
      nickname: item.nickname,
      profile_image: item.profile_image,
      date: item.created_at?.slice(0, 10),
    }))
  } catch (e) {
    console.error(e)
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchPosts()
}

const goToWrite = () => {
  router.push('/community/write')
}

const goToDetail = (articleId) => {
  router.push(`/community/${articleId}`)
}

onMounted(() => {
  fetchPosts()
})
</script> 
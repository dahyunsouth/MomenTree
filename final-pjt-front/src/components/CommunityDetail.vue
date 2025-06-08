<template>
  <div>
    <div class="p-6 bg-white rounded-3xl shadow-lg max-w-xl mx-auto mt-10">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">{{ post.title }}</h2>
        <!-- 작성자에게만 보이는 수정/삭제 버튼 -->
        <div v-if="isAuthor" class="flex space-x-2">
          <button @click="goToEdit" class="bg-yellow-500 text-white px-4 py-1 rounded hover:bg-yellow-600 transition-colors">수정</button>
          <button @click="deletePost" class="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600 transition-colors">삭제</button>
        </div>
      </div>
      <!-- 제목/작성자 구분선 -->
      <hr class="my-4 border-gray-200">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center">
          <img v-if="post.profile_image" :src="`http://localhost:8000${post.profile_image}`" class="w-8 h-8 rounded-full mr-2" />
          <span class="text-gray-600">작성자: {{ post.nickname }}</span>
        </div>
        <div class="text-gray-400 text-sm">작성일: {{ post.date }}</div>
      </div>
      <!-- 게시글 이미지 -->
      <div v-if="post.image" class="mb-6">
        <img :src="post.image.startsWith('http') ? post.image : `http://localhost:8000${post.image}`" alt="게시글 이미지" class="w-full rounded-lg shadow-md"/>
      </div>
      <div class="mb-8 whitespace-pre-line">{{ post.content }}</div>
      <!-- 게시글/댓글 구분선 -->
      <hr class="my-6 border-gray-200">

      <!-- 댓글 목록 -->
      <div class="mt-8">
        <h3 class="text-xl font-semibold mb-4">댓글</h3>
        <div v-if="comments.length === 0" class="text-gray-400 mb-4">아직 댓글이 없습니다.</div>
        <ul>
          <li v-for="comment in comments" :key="comment.id" class="mb-2 flex items-center justify-between bg-gray-100 rounded px-3 py-2">
            <div class="flex items-center">
              <img v-if="comment.profile_image" :src="`http://localhost:8000${comment.profile_image}`" class="w-6 h-6 rounded-full mr-2" />
              <span class="font-bold">{{ comment.nickname }}</span>
              <div class="ml-2">{{ comment.content }}</div>
            </div>
            <div v-if="String(currentUserId) === String(comment.user_id)">
              <button @click="startEditComment(comment)" class="text-blue-500 border border-blue-500 px-2 py-1 rounded hover:bg-blue-50 transition-colors mr-2">수정</button>
              <button @click="deleteComment(comment.id)" class="text-red-500 border border-red-500 px-2 py-1 rounded hover:bg-red-50 transition-colors">삭제</button>
            </div>
          </li>
        </ul>
        <!-- 댓글 수정 입력창 -->
        <div v-if="editingCommentId !== null" class="flex mt-2">
          <input v-model="editCommentContent" class="border rounded px-2 py-1 flex-1 mr-2" />
          <button @click="submitEditComment" class="bg-blue-500 text-white px-3 py-1 rounded font-bold">수정 완료</button>
          <button @click="cancelEditComment" class="ml-2 text-gray-500 font-bold">취소</button>
        </div>
        <!-- 댓글 작성 입력창 -->
        <div class="flex mt-4">
          <input 
            v-model="newComment" 
            placeholder="댓글을 입력하세요" 
            class="border rounded px-2 py-1 flex-1 mr-2"
            @keyup.enter="createComment"
          />
          <button @click="createComment" class="bg-[#006775] text-white px-3 py-1 rounded font-bold">등록</button>
        </div>
      </div>
    </div>
    <!-- 목록으로 버튼을 박스 밖으로 이동 -->
    <div class="max-w-xl mx-auto mt-4">
      <button @click="goBack" class="bg-[#006775] text-white px-6 py-2 rounded-full hover:bg-[#005766] transition-colors font-bold">목록으로</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const post = ref({ title: '', nickname: '', date: '', content: '' })
const comments = ref([])
const newComment = ref('')
const editingCommentId = ref(null)
const editCommentContent = ref('')
const currentUserId = ref(null)
const isAuthor = ref(false)

const fetchDetail = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/articles/${route.params.id}/`)
    post.value = {
      title: res.data.title,
      nickname: res.data.nickname,
      profile_image: res.data.profile_image,
      date: res.data.created_at?.slice(0, 10),
      content: res.data.content,
      author_id: res.data.user_id,
      image: res.data.image,
    }
    comments.value = res.data.comment_set.map(c => ({
      id: c.id,
      content: c.content,
      nickname: c.nickname || '익명',
      profile_image: c.profile_image,
      user_id: c.user_id,
    }))

    // 작성자 확인 (유저 ID 비교, 타입 강제 변환)
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const userRes = await axios.get('http://localhost:8000/accounts/profile/', { // 로그인 유저 정보 API
          headers: { Authorization: `Token ${token}` }
        })
        console.log('userRes.data:', userRes.data)
        const userObj = userRes.data.user
        currentUserId.value = userObj.id || userObj.pk || userObj.user_id
        isAuthor.value = String(currentUserId.value) === String(post.value.author_id)
      } catch (userError) {
        console.error('로그인 유저 정보 가져오기 실패:', userError)
        // 토큰은 있지만 유저 정보 가져오기 실패 시 isAuthor는 기본값(false) 유지
      }
    }

    // 디버깅용 콘솔 출력
    console.log('currentUserId:', currentUserId.value)
    console.log('post.author_id:', post.value.author_id)
    console.log('comments:', comments.value.map(c => ({id: c.id, user_id: c.user_id})))

  } catch (e) {
    alert('게시글을 불러올 수 없습니다.')
    router.push('/community')
  }
}

const createComment = async () => {
  if (!newComment.value.trim()) return
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://localhost:8000/articles/${route.params.id}/comments/`, {
      content: newComment.value
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    newComment.value = ''
    fetchDetail()
  } catch (e) {
    alert('댓글 작성 실패(로그인 필요)')
  }
}

const deleteComment = async (commentId) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://localhost:8000/articles/comments/${commentId}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    fetchDetail()
  } catch (e) {
    alert('댓글 삭제 실패(권한 필요)')
  }
}

const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

const cancelEditComment = () => {
  editingCommentId.value = null
  editCommentContent.value = ''
}

const submitEditComment = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`http://localhost:8000/articles/comments/${editingCommentId.value}/`, {
      content: editCommentContent.value
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    editingCommentId.value = null
    editCommentContent.value = ''
    fetchDetail()
  } catch (e) {
    alert('댓글 수정 실패(권한 필요)')
  }
}

const goBack = () => {
  router.push('/community')
}

const goToEdit = () => {
  router.push(`/community/${route.params.id}/edit`)
}

const deletePost = async () => {
  if (confirm('정말 게시글을 삭제하시겠습니까?')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://localhost:8000/articles/${route.params.id}/`, {
        headers: { Authorization: `Token ${token}` }
      })
      alert('게시글이 삭제되었습니다.')
      router.push('/community')
    } catch (e) {
      alert('게시글 삭제 실패(권한 필요)')
      console.error(e)
    }
  }
}

onMounted(() => {
  fetchDetail()
})
</script> 
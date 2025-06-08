<template>
  <nav class="navbar">
    <div class="nav-links">
      <router-link to="/" class="nav-link">홈</router-link>
      <router-link to="/recommend" class="nav-link">상품 추천</router-link>
      <router-link to="/products" class="nav-link">상품 조회</router-link>
      <router-link to="/search" class="nav-link">정보 검색</router-link>
      <div class="auth-links">
        <template v-if="isLoggedIn">
          <router-link to="/profile" class="nav-link">프로필</router-link>
          <a @click="handleLogout" class="nav-link logout-btn">로그아웃</a>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">로그인</router-link>
          <router-link to="/signup" class="nav-link">회원가입</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import axios from 'axios'

export default {
  name: 'NavBar',
  setup() {
    const router = useRouter()

    const isLoggedIn = computed(() => {
      return !!localStorage.getItem('token')
    })

    const handleLogout = async () => {
      try {
        const token = localStorage.getItem('token')
        await axios.post('http://localhost:8000/api/accounts/logout/', {}, {
          headers: {
            Authorization: `Token ${token}`
          }
        })
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      } catch (error) {
        console.error('로그아웃 중 오류 발생:', error)
      }
    }

    return {
      isLoggedIn,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #f8f9fa;
  padding: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.auth-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 700;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  transition: background-color 0.2s, color 0.2s;
  cursor: pointer !important;
}

.nav-link:hover {
  background-color: #e9ecef;
}

.router-link-active {
  color: #007bff;
  background-color: #e9ecef;
  font-weight: 700;
}

.logout-btn {
  color: #dc3545;
  font-weight: 700;
}

.logout-btn:hover {
  background-color: #dc3545;
  color: white;
}
</style>
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://localhost:8000'  // 백엔드 서버 URL로 수정
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const isLoggedIn = computed(() => !!token.value)
  const router = useRouter()

  // axios 기본 설정
  axios.defaults.baseURL = API_URL

  // 회원가입
  const signUp = async (payload) => {
    try {
      const formData = new FormData();
      formData.append('id', payload.id);
      formData.append('password', payload.password);
      formData.append('name', payload.name);
      formData.append('nickname', payload.nickname);
      formData.append('email', payload.email);
      formData.append('age', payload.age);
      formData.append('salary', payload.salary);
      formData.append('wealth', payload.wealth);
      formData.append('monthlyDeposit', payload.monthlyDeposit);
      formData.append('desirePeriod', payload.desirePeriod);
      formData.append('saving', JSON.stringify(payload.saving || []));
      formData.append('deposit', JSON.stringify(payload.deposit || []));
      if (payload.profileImage) {
        formData.append('profile_image', payload.profileImage);
      }
      const response = await axios.post('/accounts/signup/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      console.log('회원가입 응답:', response.data)
      
      // 회원가입 성공 시 자동 로그인
      await logIn({ 
        id: payload.id, 
        password: payload.password
      })
      
      return { success: true }
    } catch (error) {
      console.error('회원가입 실패:', error.response?.data || error.message)
      return { 
        success: false, 
        error: error.response?.data?.error || '회원가입에 실패했습니다.' 
      }
    }
  }

  // 로그인
  const logIn = async (payload) => {
    try {
      const response = await axios.post('/accounts/login/', {
        id: payload.id,
        password: payload.password
      })

      const { token: newToken, user: userData } = response.data
      
      // 토큰과 사용자 정보 저장
      token.value = newToken
      user.value = userData
      localStorage.setItem('token', newToken)
      localStorage.setItem('user', JSON.stringify(userData))

      console.log('로그인 완료')
      router.push('/')
      return { success: true }
    } catch (error) {
      console.error('로그인 실패:', error.response?.data || error.message)
      return { 
        success: false, 
        error: error.response?.data?.error || '로그인에 실패했습니다.' 
      }
    }
  }

  // 로그아웃
  const logOut = async () => {
    try {
      if (token.value) {
        await axios.post('/accounts/logout/', {}, {
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
      }

      // 상태 초기화
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')

      console.log('로그아웃 완료')
      router.push('/login')
      return { success: true }
    } catch (error) {
      console.error('로그아웃 실패:', error.response?.data || error.message)
      return { 
        success: false, 
        error: error.response?.data?.error || '로그아웃에 실패했습니다.' 
      }
    }
  }

  return { 
    user,
    token, 
    isLoggedIn, 
    signUp, 
    logIn, 
    logOut
  }
}) 
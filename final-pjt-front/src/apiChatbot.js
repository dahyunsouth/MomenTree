import axios from 'axios'

const apiChatbot = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // 반드시 /api 붙이기!
  withCredentials: false,
})

export default apiChatbot 
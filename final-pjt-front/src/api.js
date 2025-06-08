// src/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',   // 로컬 개발 서버
  withCredentials: false,
})

export default api

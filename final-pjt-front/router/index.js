import { createRouter, createWebHistory } from 'vue-router'
import ProductList from '@/components/ProductList.vue'
import VideoSearch from '@/views/VideoSearch.vue'
import VideoDetail from '@/views/VideoDetail.vue'

const routes = [
  {
    path: '/products',
    name: 'ProductList',
    component: ProductList
  },
  {
    path: '/recommend',
    name: 'RecommendProduct',
    component: RecommendProduct
  },
  {
    path: '/search',
    name: 'VideoSearch',
    component: VideoSearch
  },
  {
    path: '/video/:id',
    name: 'VideoDetail',
    component: VideoDetail
  },
  {
    path: '/video/search/:keyword',
    name: 'VideoKeywordSearch',
    component: VideoSearch
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
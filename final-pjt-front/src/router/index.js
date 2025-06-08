import { createRouter, createWebHistory } from 'vue-router'
import HeroSection from '../components/HeroSection.vue'
import CommunityBoard from '../components/CommunityBoard.vue'
import CommoditiesComparison from '../components/CommoditiesComparison.vue'
import LoginForm from '../components/LoginForm.vue'
import SignupForm from '../components/SignupForm.vue'
import BankFinder from '../components/BankFinder.vue'
import ProductList from '@/components/ProductList.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProfileEditView from '@/views/ProfileEditView.vue'
import VideoSearch from '@/components/VideoSearch.vue'
import VideoDetail from '@/components/VideoDetail.vue'
import MainView from '@/views/MainView.vue'
import CommunityDetail from '@/components/CommunityDetail.vue'
import CommunityEdit from '@/components/CommunityEdit.vue'
import CommunityWrite from '@/components/CommunityWrite.vue'
import RecommendProduct from '@/components/RecommendProduct.vue'
import SavingDetail from '@/components/SavingDetail.vue'
import DepositDetail from '@/components/DepositDetail.vue'
import PriceChart from '../components/PriceChart.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainView
  },
  {
    path: '/community',
    name: 'Community',
    component: CommunityBoard
  },
  {
    path: '/commodities',
    name: 'Commodities',
    component: CommoditiesComparison
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupForm
  },
  {
    path: '/bank-finder',
    name: 'BankFinder',
    component: BankFinder
  },
  {
    path: '/products',
    name: 'products',
    component: ProductList
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/edit',
    name: 'ProfileEdit',
    component: ProfileEditView,
    meta: { requiresAuth: true }
  },
  {
    path: '/search',
    name: 'VideoSearch',
    component: VideoSearch
  },
  {
    path: '/search/:id',
    name: 'VideoDetail',
    component: VideoDetail
  },
  {
    path: '/community',
    name: 'CommunityBoard',
    component: CommunityBoard
  },
  {
    path: '/community/:id',
    name: 'CommunityDetail',
    component: CommunityDetail
  },
  {
    path: '/community/:id/edit',
    name: 'CommunityEdit',
    component: CommunityEdit,
    meta: { requiresAuth: true }
  },
  {
    path: '/community/write',
    name: 'CommunityWrite',
    component: CommunityWrite
  },
  {
    path: '/recommend',
    name: 'RecommendProduct',
    component: RecommendProduct
  },
  {
    path: '/saving/:saving_name',
    name: 'SavingDetail',
    component: SavingDetail,
    props: true
  },
  {
    path: '/deposit/:deposit_name',
    name: 'DepositDetail',
    component: DepositDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 네비게이션 가드 추가
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    next('/login')
  } else {
    next()
  }
})

export default router 
const goToEdit = () => {
  router.push(`/community/${route.params.id}/edit`)
} 
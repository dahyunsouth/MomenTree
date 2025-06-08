<template>
  <div class="min-h-screen relative">
    <!-- Background Grid -->
    <div class="absolute inset-0 bg-grid-pattern opacity-20"></div>

    <!-- Hero Section -->
    <div class="container mx-auto px-4 pt-16 relative z-10">
      <div class="flex flex-col lg:flex-row items-center justify-between">
        <!-- Left Content -->
        <div class="lg:w-1/2 mb-10 lg:mb-0">
          <div class="relative">
            <!-- Carousel Content -->
            <div class="overflow-hidden">
              <div class="transition-transform duration-500 ease-in-out"
                :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
                <div class="flex">
                  <!-- Slide 1 -->
                  <div class="w-full flex-shrink-0">
                    <h1 class="text-6xl font-bold mb-6 text-[#1a1a1a] leading-tight tracking-tighter" style="color: darkslategray;">
                      오늘의 수입,<br />
                      내일의 자산,<br />
                      나의 나무
                    </h1>
                    <p class="text-[#333333] mb-8 text-lg max-w-lg tracking-tight" style="color: darkslategray;">
                      맞춤형 추천으로<br />
                      나에게 꼭 맞는 예적금을 찾아요
                    </p>
                    <button
                      @click="goToRecommend"
                      class="border-2 border-[#85B554] text-[#85B554] px-8 py-3 rounded-full hover:bg-[#85B554] hover:text-white transition-all duration-300 font-bold flex items-center">
                      상품 추천받으러 가기
                      <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                  <!-- Slide 2 -->
                  <div class="w-full flex-shrink-0">
                    <h1 class="text-6xl font-bold mb-6 text-[#1a1a1a] leading-tight tracking-tighter" style="color: darkslategray;">
                      결정의 순간,<br />
                      자라나는 금융,<br />
                      MomenTree
                    </h1>
                    <p class="text-[#333333] mb-8 text-lg max-w-lg tracking-tight" style="color: darkslategray;">
                      당신의 선택 하나하나가<br />
                      금융 성장의 숲을 키웁니다
                    </p>
                    <button
                      @click="goToProductList"
                      class="border-2 border-[#85B554] text-[#85B554] px-8 py-3 rounded-full hover:bg-[#85B554] hover:text-white transition-all duration-300 font-bold flex items-center">
                      상품 조회하러 가기
                      <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                  <!-- Slide 3 -->
                  <div class="w-full flex-shrink-0">
                    <h1 class="text-6xl font-bold mb-6 text-[#1a1a1a] leading-tight tracking-tighter" style="color: darkslategray;">
                      집 근처,<br />
                      직장 근처,<br />
                      은행 어디 있지?
                    </h1>
                    <p class="text-[#333333] mb-8 text-lg max-w-lg tracking-tight" style="color: darkslategray;">
                      현재 위치를 기반으로<br />
                      가장 가까운 은행을 안내해드려요
                    </p>
                    <button
                      @click="goToBankFinder"
                      class="border-2 border-[#85B554] text-[#85B554] px-8 py-3 rounded-full hover:bg-[#85B554] hover:text-white transition-all duration-300 font-bold flex items-center">
                      주변 은행 찾으러 가기
                      <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                  <!-- Slide 4 -->
                  <div class="w-full flex-shrink-0">
                    <h1 class="text-6xl font-bold mb-6 text-[#1a1a1a] leading-tight tracking-tighter" style="color: darkslategray;">
                      금이 올랐을까?<br />
                      은이 올랐을까?<br />
                      지금이 적기일까?
                    </h1>
                    <p class="text-[#333333] mb-8 text-lg max-w-lg tracking-tight" style="color: darkslategray;">
                      기간별 시세를 분석해<br />
                      현물 상품을 똑똑하게 비교해요
                    </p>
                    <button
                      @click="goToPriceChart"
                      class="border-2 border-[#85B554] text-[#85B554] px-8 py-3 rounded-full hover:bg-[#85B554] hover:text-white transition-all duration-300 font-bold flex items-center">
                      현물 가격 비교하러 가기
                      <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                  <!-- Slide 5 -->
                  <div class="w-full flex-shrink-0">
                    <h1 class="text-6xl font-bold mb-6 text-[#1a1a1a] leading-tight tracking-tighter" style="color: darkslategray;">
                      내가 찜한,<br />
                      관심 있는<br />
                      그 종목의 소식
                    </h1>
                    <p class="text-[#333333] mb-8 text-lg max-w-lg tracking-tight" style="color: darkslategray;">
                      유튜브 영상을 통해<br />
                      관심 종목 정보를 한눈에 확인해요
                    </p>
                    <button
                      @click="goToVideoSearch"
                      class="border-2 border-[#85B554] text-[#85B554] px-8 py-3 rounded-full hover:bg-[#85B554] hover:text-white transition-all duration-300 font-bold flex items-center">
                      정보 검색하러 가기
                      <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                  <!-- Slide 6 -->
                  <div class="w-full flex-shrink-0">
                    <h1 class="text-6xl font-bold mb-6 text-[#1a1a1a] leading-tight tracking-tighter" style="color: darkslategray;">
                      같이 궁금한,<br />
                      같이 나누는,<br />
                      우리의 이야기
                    </h1>
                    <p class="text-[#333333] mb-8 text-lg max-w-lg tracking-tight" style="color: darkslategray;">
                      다른 사용자들과 소통하며<br />
                      금융 정보를 나눌 수 있어요
                    </p>
                    <button
                      @click="goToCommunity"
                      class="border-2 border-[#85B554] text-[#85B554] px-8 py-3 rounded-full hover:bg-[#85B554] hover:text-white transition-all duration-300 font-bold flex items-center">
                      커뮤니티 바로 가기
                      <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-4">
            <!-- Navigation Buttons -->
            <div class="flex space-x-2">
              <button @click="prevSlide" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button @click="nextSlide" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Users Section -->
          <div class="mt-16">
            <div class="flex items-center mb-4">
              <div class="flex -space-x-3">
                <img src="@/assets/people_img/김재유.png" class="w-10 h-10 rounded-full border-2 border-[#1a1a1a]"
                  alt="User" />
                <img src="@/assets/people_img/남다현.png" class="w-10 h-10 rounded-full border-2 border-[#1a1a1a]"
                  alt="User" />
                <img src="@/assets/people_img/서연희.png" class="w-10 h-10 rounded-full border-2 border-[#1a1a1a]"
                  alt="User" />
                <img src="@/assets/people_img/윤설아.png" class="w-10 h-10 rounded-full border-2 border-[#1a1a1a]"
                  alt="User" />
              </div>
              <div class="ml-6">
                <h3 class="text-4xl font-bold text-white" style="color: darkslategray;">2.5K +</h3>
                <p class="text-white/70" style="color: darkslategray;">2,500명의 금융 선택, 이제는 당신 차례입니다.</p>
              </div>
            </div>
          </div>

          <!-- Partners -->
          <div class="mt-12">
            <p class="text-white/50 mb-4" style="color: darkslategray;">저희의 소중한 파트너 및 제휴사를 만나보세요</p>
            <div class="relative w-full h-16 overflow-hidden">
              <div ref="containerRef" class="infinite-scroll-container flex items-center gap-12"
                :style="{ transform: `translateX(${position}px)` }">
                <!-- 첫 번째 세트 -->
                <img v-for="image in bankImages" :key="image.alt" :src="image.src" :alt="image.alt"
                  class="h-8 w-auto object-contain" />
                <!-- 두 번째 세트 (무한 스크롤을 위한 복제) -->
                <img v-for="image in bankImages" :key="image.alt + '-clone'" :src="image.src" :alt="image.alt"
                  class="h-8 w-auto object-contain" />
              </div>
            </div>
          </div>
        </div>

        <!-- Right Content (Card) -->
        <div class="lg:w-1/2 relative flex items-center justify-center">
          <div class="floating-character w-[800px] relative">
            <img :src="characterImage" alt="MomenTree Character" class="w-full h-auto floating-animation scale-125" />
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <!-- <div class="container mx-auto px-4 py-16">
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold mb-4">더 스마트한 금융<br/>더 나은 선택</h2>
        <p class="text-gray-600">모든 금융 서비스를 한 곳에서<br/>쉽고 편리하게 관리하세요</p>
      </div> -->

    <!-- Feature Cards -->
    <!-- <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"> -->
    <!-- Card 1 -->
    <!-- <div class="bg-white p-6 rounded-xl shadow-lg">
          <div class="mb-4">
            <img src="@/assets/sync-icon.svg" alt="Sync" class="w-12 h-12"/>
          </div>
          <h3 class="text-xl font-semibold mb-2">안전한 계좌 연동으로<br/>한눈에 보는 자산</h3>
          <p class="text-gray-600">은행 계좌, 카드, 투자 내역을 안전하게 연동하여 한눈에 확인할 수 있습니다.</p>
        </div> -->

    <!-- Card 2 -->
    <!-- <div class="bg-white p-6 rounded-xl shadow-lg">
          <div class="mb-4">
            <img src="@/assets/ai-icon.svg" alt="AI" class="w-12 h-12"/>
          </div>
          <h3 class="text-xl font-semibold mb-2">AI 기반 맞춤형<br/>금융 인사이트</h3>
          <p class="text-gray-600">소비 패턴을 분석하고 개인화된 금융 추천으로 더 나은 자산 관리를 도와드립니다.</p>
        </div> -->

    <!-- Card 3 -->
    <!-- <div class="bg-white p-6 rounded-xl shadow-lg">
          <div class="mb-4">
            <img src="@/assets/globe-icon.svg" alt="Global" class="w-12 h-12"/>
          </div>
          <h3 class="text-xl font-semibold mb-2">간편한 계좌 개설<br/>빠른 시작</h3>
          <p class="text-gray-600">복잡한 서류 없이 몇 분 만에 계좌 개설이 가능합니다. 지금 바로 시작하세요.</p>
        </div>
      </div>
    </div> -->

    <!-- Join Section -->
    <!-- <div class="container mx-auto px-4 py-16">
      <div class="bg-[#006775] text-white p-12 rounded-3xl text-center">
        <h2 class="text-3xl font-bold mb-4">지금 바로 시작하세요<br/>더 나은 금융 생활</h2>
        <p class="mb-8">모든 카드와 계좌를 한 곳에서<br/>더 스마트하게 관리하세요</p>
        <button class="bg-white text-[#006775] px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors">
          시작하기
        </button>
      </div>
    </div> --->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import characterImage from '@/assets/character_img/character_1.png'

// 캐러셀 관련 상태
const currentSlide = ref(0)
const totalSlides = 6

// 캐러셀 제어 함수
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % totalSlides
}

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + totalSlides) % totalSlides
}

// 자동 슬라이드 기능
let autoSlideInterval
const startAutoSlide = () => {
  autoSlideInterval = setInterval(() => {
    nextSlide()
  }, 5000) // 5초마다 다음 슬라이드로 이동
}

const stopAutoSlide = () => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
  }
}

const containerRef = ref(null)
const position = ref(0)
let animationId = null

const animate = () => {
  position.value -= 0.5

  // 컨테이너의 절반을 넘어가면 처음으로 리셋
  if (containerRef.value && position.value <= -containerRef.value.scrollWidth / 2) {
    position.value = 0
  }

  animationId = requestAnimationFrame(animate)
}

onMounted(() => {
  startAutoSlide()
  animationId = requestAnimationFrame(animate)
})

onUnmounted(() => {
  stopAutoSlide()
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})

// 은행 이미지 import
const bankImages = [
  { src: new URL('@/assets/bank_img/국민은행.png', import.meta.url).href, alt: '국민은행' },
  { src: new URL('@/assets/bank_img/신한은행.png', import.meta.url).href, alt: '신한은행' },
  { src: new URL('@/assets/bank_img/우리은행.png', import.meta.url).href, alt: '우리은행' },
  { src: new URL('@/assets/bank_img/하나은행.png', import.meta.url).href, alt: '하나은행' },
  { src: new URL('@/assets/bank_img/농협은행주식회사.png', import.meta.url).href, alt: '농협은행' },
  { src: new URL('@/assets/bank_img/수협은행.png', import.meta.url).href, alt: '수협은행' },
  { src: new URL('@/assets/bank_img/토스뱅크 주식회사.png', import.meta.url).href, alt: '토스뱅크' },
  { src: new URL('@/assets/bank_img/주식회사 카카오뱅크.png', import.meta.url).href, alt: '카카오뱅크' },
  { src: new URL('@/assets/bank_img/주식회사 케이뱅크.png', import.meta.url).href, alt: '케이뱅크' },
  { src: new URL('@/assets/bank_img/한국산업은행.png', import.meta.url).href, alt: '한국산업은행' },
  { src: new URL('@/assets/bank_img/중소기업은행.png', import.meta.url).href, alt: '중소기업은행' },
  { src: new URL('@/assets/bank_img/경남은행.png', import.meta.url).href, alt: '경남은행' },
  { src: new URL('@/assets/bank_img/전북은행.png', import.meta.url).href, alt: '전북은행' },
  { src: new URL('@/assets/bank_img/제주은행.png', import.meta.url).href, alt: '제주은행' },
  { src: new URL('@/assets/bank_img/광주은행.png', import.meta.url).href, alt: '광주은행' },
  { src: new URL('@/assets/bank_img/부산은행.png', import.meta.url).href, alt: '부산은행' },
  { src: new URL('@/assets/bank_img/아이엠뱅크.png', import.meta.url).href, alt: '아이엠뱅크' },
  { src: new URL('@/assets/bank_img/한국스탠다드차타드은행.png', import.meta.url).href, alt: '한국스탠다드차타드은행' },
]

// 라우터 관련 설정
const router = useRouter()
const goToRecommend = () => {
  router.push('/recommend')
}
const goToProductList = () => {
  router.push('/products') // 라우터 name이 'ProductList'일 때
}
const goToBankFinder = () => {
  router.push('/bank-finder') // 라우터 path 또는 name에 맞게 수정
}
const goToPriceChart = () => {
  router.push('/commodities') // 라우터 path 또는 name에 맞게 수정
}
const goToVideoSearch = () => {
  router.push('/search') // 라우터 path 또는 name에 맞게 수정
}
const goToCommunity = () => {
  router.push('/community') // 라우터 path 또는 name에 맞게 수정
}
</script>

<style scoped>
.bg-grid-pattern {
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  background-position: center center;
}

/* Glass morphism effect for navigation */
nav {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 캐릭터 두둥실 애니메이션 */
.floating-animation {
  animation: floating 3s ease-in-out infinite;
  filter: drop-shadow(0 10px 15px rgba(0, 0, 0, 0.1));
}

@keyframes floating {

  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }

  50% {
    transform: translateY(-20px) rotate(2deg);
  }
}

.floating-character {
  transition: all 0.3s ease;
}

.floating-character:hover {
  transform: scale(1.05);
}

/* 캐러셀 애니메이션 */
.carousel-slide-enter-active,
.carousel-slide-leave-active {
  transition: all 0.5s ease;
}

.carousel-slide-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.carousel-slide-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.infinite-scroll-container {
  transition: transform 0s linear;
}

/* position이 특정 값에 도달하면 순간적으로 처음 위치로 리셋 */
@keyframes resetPosition {
  from {
    transform: translateX(var(--current-position));
  }

  to {
    transform: translateX(0);
  }
}
</style>
<template>
  <main class="max-w-7xl mx-auto px-4 md:px-8 py-8 relative overflow-hidden">
    <!-- 3D 배경 요소 추가 -->
    <div class="absolute inset-0 -z-10">
      <!-- 메인 그라데이션 배경 -->
      <div class="absolute inset-0 bg-gradient-to-br from-white via-blue-50/80 to-purple-100/80"></div>
      
      <!-- 3D 효과를 위한 블러 요소들 -->
      <div class="absolute -top-20 -left-32 w-[600px] h-[600px] bg-blue-300/40 rounded-full blur-[100px] animate-pulse"></div>
      <div class="absolute top-40 -right-32 w-[600px] h-[600px] bg-purple-300/30 rounded-full blur-[100px] animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute -bottom-20 left-1/3 w-[500px] h-[500px] bg-emerald-200/30 rounded-full blur-[100px] animate-pulse" style="animation-delay: 2s;"></div>
      
      <!-- 추가 장식 요소 -->
      <div class="absolute top-1/4 right-1/4 w-4 h-4 bg-blue-400/30 rounded-full blur-sm"></div>
      <div class="absolute bottom-1/3 left-1/4 w-6 h-6 bg-purple-400/30 rounded-full blur-sm"></div>
      <div class="absolute top-1/3 left-1/3 w-3 h-3 bg-emerald-400/30 rounded-full blur-sm"></div>
    </div>

    <div class="relative backdrop-blur-[2px]">
      <!-- Carousel Container -->
      <div class="overflow-hidden">
        <div class="flex transition-transform duration-500 ease-in-out" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <!-- Slide 1 -->
          <div class="w-full flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex-1 max-w-lg z-10">
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 leading-tight mb-4">
                  나의 금융,<br>
                  나의 나무,<br>
                  나의 이야기
                </h1>
                
                <p class="text-lg md:text-xl text-gray-600 mb-16 leading-relaxed">
                  순간을 심고, 추억을 키우다<br>
                  함께 자라는 숲, MomenTree
                </p>
                
                <div class="flex items-center space-x-3">
                  <button class="bg-white hover:bg-gray-50 text-gray-900 px-6 py-3 rounded-full text-base font-medium transition-all shadow-lg hover:shadow-xl">
                    자세히 보기
                  </button>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="prevSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="이전 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                    <button 
                      @click="nextSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="다음 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <div class="flex-1 flex justify-center items-center">
                <div class="hidden lg:block">
                  <GradientCircle :size="'large'" />
                </div>
                <div class="lg:hidden">
                  <GradientCircle :size="'medium'" :opacity="0.8" />
                </div>
              </div>
            </div>
          </div>

          <!-- Slide 2 -->
          <div class="w-full flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex-1 max-w-lg z-10">
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 leading-tight mb-4">
                  금융의 시작,<br>
                  당신의 목표
                </h1>
                
                <p class="text-lg md:text-xl text-gray-600 mb-16 leading-relaxed">
                  나만의 금융 목표를 설정하고<br>
                  체계적으로 관리해보세요
                </p>
                
                <div class="flex items-center space-x-3">
                  <button class="bg-white hover:bg-gray-50 text-gray-900 px-6 py-3 rounded-full text-base font-medium transition-all shadow-lg hover:shadow-xl">
                    자세히 보기
                  </button>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="prevSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="이전 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                    <button 
                      @click="nextSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="다음 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <div class="flex-1 flex justify-center items-center">
                <div class="hidden lg:block">
                  <GradientCircle :size="'large'" :color="'blue'" />
                </div>
                <div class="lg:hidden">
                  <GradientCircle :size="'medium'" :color="'blue'" :opacity="0.8" />
                </div>
              </div>
            </div>
          </div>

          <!-- Slide 3 -->
          <div class="w-full flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex-1 max-w-lg z-10">
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 leading-tight mb-4">
                  맞춤형 상품,<br>
                  스마트한 선택
                </h1>
                
                <p class="text-lg md:text-xl text-gray-600 mb-16 leading-relaxed">
                  당신에게 딱 맞는<br>
                  금융상품을 찾아보세요
                </p>
                
                <div class="flex items-center space-x-3">
                  <button class="bg-white hover:bg-gray-50 text-gray-900 px-6 py-3 rounded-full text-base font-medium transition-all shadow-lg hover:shadow-xl">
                    자세히 보기
                  </button>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="prevSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="이전 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                    <button 
                      @click="nextSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="다음 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <div class="flex-1 flex justify-center items-center">
                <div class="hidden lg:block">
                  <GradientCircle :size="'large'" :color="'purple'" />
                </div>
                <div class="lg:hidden">
                  <GradientCircle :size="'medium'" :color="'purple'" :opacity="0.8" />
                </div>
              </div>
            </div>
          </div>

          <!-- Slide 4 -->
          <div class="w-full flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex-1 max-w-lg z-10">
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 leading-tight mb-4">
                  함께 성장하는<br>
                  금융 커뮤니티
                </h1>
                
                <p class="text-lg md:text-xl text-gray-600 mb-16 leading-relaxed">
                  다양한 경험과 정보를<br>
                  공유해보세요
                </p>
                
                <div class="flex items-center space-x-3">
                  <button class="bg-white hover:bg-gray-50 text-gray-900 px-6 py-3 rounded-full text-base font-medium transition-all shadow-lg hover:shadow-xl">
                    자세히 보기
                  </button>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="prevSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="이전 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                    <button 
                      @click="nextSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="다음 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <div class="flex-1 flex justify-center items-center">
                <div class="hidden lg:block">
                  <GradientCircle :size="'large'" :color="'green'" />
                </div>
                <div class="lg:hidden">
                  <GradientCircle :size="'medium'" :color="'green'" :opacity="0.8" />
                </div>
              </div>
            </div>
          </div>

          <!-- Slide 5 -->
          <div class="w-full flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex-1 max-w-lg z-10">
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 leading-tight mb-4">
                  실시간 정보로<br>
                  스마트한 결정
                </h1>
                
                <p class="text-lg md:text-xl text-gray-600 mb-16 leading-relaxed">
                  최신 금융 정보와<br>
                  전문가의 조언을 확인하세요
                </p>
                
                <div class="flex items-center space-x-3">
                  <button class="bg-white hover:bg-gray-50 text-gray-900 px-6 py-3 rounded-full text-base font-medium transition-all shadow-lg hover:shadow-xl">
                    자세히 보기
                  </button>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="prevSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="이전 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                    <button 
                      @click="nextSlide" 
                      class="w-10 h-10 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20 transition-colors"
                      aria-label="다음 슬라이드"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <div class="flex-1 flex justify-center items-center">
                <div class="hidden lg:block">
                  <GradientCircle :size="'large'" :color="'orange'" />
                </div>
                <div class="lg:hidden">
                  <GradientCircle :size="'medium'" :color="'orange'" :opacity="0.8" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import GradientCircle from './GradientCircle.vue'

const currentSlide = ref(0)
const totalSlides = 5
const autoplayInterval = ref(null)

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % totalSlides
}

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + totalSlides) % totalSlides
}

const goToSlide = (index) => {
  currentSlide.value = index
}

const startAutoplay = () => {
  autoplayInterval.value = setInterval(() => {
    nextSlide()
  }, 5000) // 5초마다 자동 전환
}

const stopAutoplay = () => {
  if (autoplayInterval.value) {
    clearInterval(autoplayInterval.value)
  }
}

onMounted(() => {
  startAutoplay()
})

onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
.carousel-slide {
  transition: transform 0.5s ease-in-out;
}
</style>
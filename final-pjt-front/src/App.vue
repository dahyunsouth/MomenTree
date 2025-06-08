<template>
  <div class="bg-gradient-pattern min-h-screen relative overflow-hidden">
    <!-- 커서 효과 주석 처리 -->
    <!-- <div ref="cursor" class="cursor-image"></div>
    <div ref="cursorFollower" class="cursor-follower"></div> -->
    <!-- 꽃가루 컨테이너 추가 -->
    <div ref="particlesContainer" class="particles-container"></div>
    
    <Header />
    <div class="max-w-7xl mx-auto px-4 md:px-8 py-8">
      <router-view></router-view>
    </div>
    <ChatBot />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import cursorImage from './assets/sprout-cursor.svg'
import ChatBot from './components/ChatBot.vue'

const cursor = ref(null)
const cursorFollower = ref(null)
const particlesContainer = ref(null)

let mouseX = 0
let mouseY = 0
let cursorX = 0
let cursorY = 0
let followerX = 0
let followerY = 0

// 꽃가루 파티클 생성 함수
const createParticle = (x, y) => {
  const particle = document.createElement('div')
  particle.className = 'particle'
  
  // 랜덤 크기와 회전
  const size = Math.random() * 8 + 4
  const rotation = Math.random() * 360
  const xVelocity = (Math.random() - 0.5) * 100
  const yVelocity = Math.random() * 50 + 100
  
  particle.style.width = `${size}px`
  particle.style.height = `${size}px`
  particle.style.left = `${x}px`
  particle.style.top = `${y}px`
  
  // 랜덤 색상 (초록색 계열)
  const hue = 120 + Math.random() * 40
  const saturation = 60 + Math.random() * 40
  const lightness = 70 + Math.random() * 20
  particle.style.backgroundColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`
  
  particlesContainer.value.appendChild(particle)
  
  let startTime = performance.now()
  
  function animateParticle(currentTime) {
    const elapsed = (currentTime - startTime) / 1000 // 초 단위로 변환
    
    if (elapsed < 1) {
      const progress = elapsed
      const currentX = x + xVelocity * progress
      const currentY = y + yVelocity * progress + (100 * progress * progress) // 중력 효과
      const currentRotation = rotation + (360 * progress)
      const opacity = 1 - progress
      
      particle.style.transform = `translate(${currentX - x}px, ${currentY - y}px) rotate(${currentRotation}deg)`
      particle.style.opacity = opacity
      
      requestAnimationFrame(animateParticle)
    } else {
      particle.remove()
    }
  }
  
  requestAnimationFrame(animateParticle)
}

// 마우스 이동 시 파티클 생성
const onMouseMove = (e) => {
  mouseX = e.clientX
  mouseY = e.clientY
  
  // 10% 확률로 파티클 생성
  if (Math.random() < 0.1) {
    createParticle(mouseX, mouseY)
  }
}

const animate = () => {
  // 커서 애니메이션 주석 처리
  // // 메인 커서
  // cursorX += (mouseX - cursorX) * 0.2
  // cursorY += (mouseY - cursorY) * 0.2
  // if (cursor.value) {
  //   cursor.value.style.transform = `translate(${cursorX}px, ${cursorY}px) translate(-50%, -50%)`
  // }

  // // 팔로워 커서
  // followerX += (mouseX - followerX) * 0.1
  // followerY += (mouseY - followerY) * 0.1
  // if (cursorFollower.value) {
  //   cursorFollower.value.style.transform = `translate(${followerX}px, ${followerY}px) translate(-50%, -50%)`
  // }

  requestAnimationFrame(animate)
}

onMounted(() => {
  document.addEventListener('mousemove', onMouseMove)
  animate()
  
  // 커서 숨기기 제거
  // document.body.style.cursor = 'none'
})

onUnmounted(() => {
  document.removeEventListener('mousemove', onMouseMove)
  // document.body.style.cursor = 'auto' // 이 부분도 제거
})
</script>

<style>
.bg-gradient-pattern {
  background: url('./assets/Background.png') no-repeat center center fixed;
  background-size: cover;
}

/* 커서 스타일 */
.cursor-image {
  width: 32px;
  height: 32px;
  background-image: url('./assets/sprout-cursor.svg');
  background-size: contain;
  background-repeat: no-repeat;
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  transform-origin: center center;
  transition: transform 0.1s ease;
  filter: drop-shadow(0 2px 4px rgba(0, 100, 0, 0.2));
  animation: cursor-bounce 1s ease-in-out infinite;
}

.cursor-follower {
  width: 60px;
  height: 60px;
  background: rgba(144, 238, 144, 0.1);
  border: 2px solid rgba(144, 238, 144, 0.2);
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 9998;
  transition: all 0.3s ease;
  animation: follower-pulse 2s ease-in-out infinite;
}

@keyframes cursor-bounce {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-2px) rotate(2deg);
  }
}

@keyframes follower-pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
}

/* 링크나 버튼에 호버했을 때 효과 */
a:hover ~ .cursor-image,
button:hover ~ .cursor-image {
  transform: scale(1.2) rotate(-10deg);
}

a:hover ~ .cursor-follower,
button:hover ~ .cursor-follower {
  width: 70px;
  height: 70px;
  background: rgba(144, 238, 144, 0.15);
  border-color: rgba(144, 238, 144, 0.4);
}

/* 전역 스타일 */
body, #app {
  margin: 0;
  padding: 0;
  color: #1d1d1f;
}

#app {
  min-height: 100vh;
}

/* 링크와 버튼의 커서 스타일 제거 */
/* a, button {
  cursor: none;
} */

/* 파티클 컨테이너 */
.particles-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9997;
}

/* 파티클 스타일 */
.particle {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  transition: transform 0.016s linear;
}
</style>
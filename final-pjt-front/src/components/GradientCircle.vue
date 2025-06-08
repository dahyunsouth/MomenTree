<template>
  <div class="relative">
    <!-- Main Gradient Circle -->
    <div 
      :class="[circleClasses, gradientClass]"
      :style="{ opacity: opacity }"
    ></div>
    
    <!-- Decorative Elements -->
    <div v-if="size === 'large'" class="absolute top-4 right-4 w-12 h-12 bg-white bg-opacity-30 rounded-full animate-pulse"></div>
    <div v-if="size === 'large'" class="absolute bottom-8 left-8 w-8 h-8 bg-white bg-opacity-20 rounded-full animate-pulse" style="animation-delay: 1s;"></div>
    <div v-if="size === 'large'" class="absolute top-1/2 left-4 w-6 h-6 bg-white bg-opacity-25 rounded-full animate-pulse" style="animation-delay: 2s;"></div>
  </div>
</template>

<script>
export default {
  name: 'GradientCircle',
  props: {
    size: {
      type: String,
      default: 'large',
      validator: (value) => ['small', 'medium', 'large', 'xlarge'].includes(value)
    },
    opacity: {
      type: Number,
      default: 0.9
    },
    color: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'blue', 'purple', 'green', 'orange'].includes(value)
    }
  },
  computed: {
    circleClasses() {
      const sizeClasses = {
        small: 'w-48 h-48',
        medium: 'w-64 h-64 md:w-80 md:h-80',
        large: 'w-80 h-80 xl:w-96 xl:h-96',
        xlarge: 'w-96 h-96 xl:w-[28rem] xl:h-[28rem]'
      }
      return sizeClasses[this.size] || sizeClasses.large
    },
    gradientClass() {
      const gradients = {
        default: 'bg-gradient-to-br from-moment-400 via-moment-400 to-purple-400',
        blue: 'bg-gradient-to-br from-blue-400 via-blue-500 to-indigo-500',
        purple: 'bg-gradient-to-br from-purple-400 via-purple-500 to-pink-500',
        green: 'bg-gradient-to-br from-green-400 via-green-500 to-emerald-500',
        orange: 'bg-gradient-to-br from-orange-400 via-orange-500 to-amber-500'
      }
      return `${gradients[this.color]} rounded-full animate-pulse-slow`
    }
  }
}
</script>
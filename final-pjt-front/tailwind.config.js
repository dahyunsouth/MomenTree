/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        'moment': {
          400: '#B3DD62',
          500: '#9AC948', // 약간 더 어두운 톤
        }
      },
      animation: {
        'pulse-slow': 'pulse-slow 4s ease-in-out infinite',
      },
      keyframes: {
        'pulse-slow': {
          '0%, 100%': {
            transform: 'scale(1)',
            opacity: '0.9',
          },
          '50%': {
            transform: 'scale(1.05)',
            opacity: '0.7',
          },
        }
      }
    },
  },
  plugins: [],
}
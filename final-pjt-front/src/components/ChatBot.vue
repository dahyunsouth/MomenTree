<template>
  <div class="chatbot-container" :class="{ open: isOpen }">
    <div class="chatbot-toggle" @click="toggleChatbot">
      <span v-if="!isOpen">💬</span>
      <span v-else>✖</span>
    </div>
    <transition name="fade">
      <div v-if="isOpen" class="chatbot-box">
        <div class="chatbot-header">금융 챗봇</div>
        <!-- 소비 성향 테스트가 아닐 때만 기존 메시지/폼 영역 표시 -->
        <div>
          <div class="chatbot-messages" ref="messagesBox">
            <!-- 기존 메시지 반복문 -->
            <div v-for="(msg, idx) in messages" :key="idx">
              <div :class="['message', msg.role]">
                <span v-if="msg.role==='bot'">🤖</span>
                <span v-else>🧑</span>
                <span class="msg-text">{{ msg.text }}</span>
              </div>
              <!-- 선택지는 message div 바깥에 위치 -->
              <div
                v-if="msg.choices && idx === messages.length - 1 && msg.role === 'bot'"
                class="choices-container"
              >
                <button
                  v-for="(choice, cidx) in msg.choices"
                  :key="cidx"
                  class="chatbot-btn"
                  @click="selectConsumptionChoice(cidx)"
                >
                  {{ choice }}
                </button>
              </div>
            </div>
            <!-- 버튼 영역: step이 idle일 때만 보이게, 메시지 바로 아래에 위치 -->
            <div
              v-if="step === 'idle'"
              class="flex flex-col items-center mt-4 gap-2"
              style="margin-bottom: 0.5rem;"
            >
              <button class="calculator-btn" @click="showTypeSelect">예적금 계산기</button>
              <button class="calculator-btn" @click="startConsumptionTest">소비 성향 테스트</button>
            </div>
          </div>
          <form v-if="['select','input_month','input_amount','input_deposit_amount'].includes(step)" class="chatbot-input-area" @submit.prevent="handleUserInput">
            <template v-if="step==='select'">
              <select v-model="selectedProduct" class="chatbot-select">
                <option disabled value="">관심 {{typeKor}} 상품을 선택하세요</option>
                <option v-for="item in productList" :key="item.fin_prdt_nm" :value="item.fin_prdt_nm">
                  {{ item.kor_co_nm }} - {{ item.fin_prdt_nm }}
                </option>
              </select>
              <button type="submit" class="chatbot-btn">선택</button>
            </template>
            <template v-else-if="step==='input_month'">
              <input v-model="inputMonth" type="number" min="1" max="36" class="chatbot-input" placeholder="가입 개월 수(예: 12)" />
              <button type="submit" class="chatbot-btn">입력</button>
            </template>
            <template v-else-if="step==='input_amount'">
              <input v-model="inputAmount" type="number" step="1000" class="chatbot-input" placeholder="월 납입금(예: 300,000)" />
              <button type="submit" class="chatbot-btn">입력</button>
            </template>
            <template v-else-if="step==='input_deposit_amount'">
              <input v-model="inputAmount" type="number" step="1000" class="chatbot-input" placeholder="예치금액(예: 100,000)" />
              <button type="submit" class="chatbot-btn">입력</button>
            </template>
          </form>
        </div>
        <!-- 소비 성향 테스트일 때만 표시 -->
        <ConsumptionTest v-if="step === 'consumption'" @close="closeConsumptionTest" />
        <!-- 예적금 유형 선택 버튼: step이 'type'일 때만 보이게 -->
        <div
          v-if="step === 'type'"
          class="flex justify-center gap-2 type-select-btns"
        >
          <button class="chatbot-btn" @click="selectType('deposit')">예금</button>
          <button class="chatbot-btn" @click="selectType('saving')">적금</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import apiChatbot from '../apiChatbot'
import { defineComponent } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const messages = ref([
  { role: 'bot', text: '무엇을 도와드릴까요?' }
])
const step = ref('idle')
const type = ref('') // 'deposit' or 'saving'
const typeKor = ref('')
const productList = ref([])
const selectedProduct = ref('')
const inputMonth = ref('')
const inputAmount = ref('')
const messagesBox = ref(null)

const showTypeSelect = () => {
  step.value = 'type'
  messages.value.push({ role: 'bot', text: '예금과 적금 중 어떤 상품을 계산할까요?' })
  scrollToBottom()
}

const selectType = async (selected) => {
  type.value = selected
  typeKor.value = selected === 'deposit' ? '예금' : '적금'
  messages.value.push({ role: 'bot', text: `로그인한 사용자의 관심 ${typeKor.value} 상품을 불러오는 중입니다...` })
  // 관심 상품 불러오기
  await fetchInterestProducts()
  if (productList.value.length === 0) {
    messages.value.push({ role: 'bot', text: `관심 ${typeKor.value}이 없습니다. 관심 상품을 먼저 등록해주세요.` })
    step.value = 'idle'
    scrollToBottom()
    return
  }
  messages.value.push({ role: 'bot', text: `관심 ${typeKor.value} 상품 중에서 선택해주세요.` })
  step.value = 'select'
  selectedProduct.value = ''
  scrollToBottom()
}

const fetchInterestProducts = async () => {
  try {
    const token = localStorage.getItem('token')
    const url = type.value === 'deposit' ? '/interest/deposit/' : '/interest/saving/'
    const res = await apiChatbot.get(url, {
      headers: { Authorization: `Token ${token}` }
    })
    productList.value = res.data
  } catch (e) {
    productList.value = []
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesBox.value) {
      // 첫 번째 시도
      messagesBox.value.scrollTop = messagesBox.value.scrollHeight
      // 렌더링이 늦게 끝나는 경우를 위해 한 번 더
      setTimeout(() => {
        if (messagesBox.value) {
          messagesBox.value.scrollTop = messagesBox.value.scrollHeight
        }
      }, 50)
    }
  })
}

const handleUserInput = async () => {
  if (step.value === 'select') {
    if (!selectedProduct.value) return
    messages.value.push({ role: 'user', text: selectedProduct.value })
    messages.value.push({ role: 'bot', text: '가입 개월 수(예: 12)를 입력해주세요.' })
    step.value = 'input_month'
    inputMonth.value = ''
    scrollToBottom()
    return
  }
  if (step.value === 'input_month') {
    const allowedMonths = [3, 6, 12, 24, 36]
    const month = Number(inputMonth.value)
    if (!month || !allowedMonths.includes(month)) {
      messages.value.push({ role: 'bot', text: '가입 개월 수는 3, 6, 12, 24, 36 중 하나만 입력할 수 있습니다.' })
      inputMonth.value = ''
      scrollToBottom()
      return
    }
    messages.value.push({ role: 'user', text: `${month}개월` })
    if (type.value === 'deposit') {
      messages.value.push({ role: 'bot', text: '예치금액(숫자, 예: 100,000)을 입력해주세요.' })
      step.value = 'input_deposit_amount'
    } else {
      messages.value.push({ role: 'bot', text: '월 납입금(숫자, 예: 300,000)을 입력해주세요.' })
      step.value = 'input_amount'
    }
    inputAmount.value = ''
    scrollToBottom()
    return
  }

  if (step.value === 'input_amount') {
    const amount = Number(inputAmount.value)
    if (!amount || isNaN(amount) || amount < 10000) {
      messages.value.push({ role: 'bot', text: '월 납입금은 10,000원 이상 입력해야 합니다.' })
      inputAmount.value = ''
      scrollToBottom()
      return
    }
    messages.value.push({ role: 'user', text: `${amount}원` })
    // 적금 계산 API 호출
    try {
      const token = localStorage.getItem('token')
      const res = await apiChatbot.post('/calculate_saving_maturity/', {
        saving_name: selectedProduct.value,
        save_trm: inputMonth.value,
        monthly_amount: inputAmount.value
      }, {
        headers: { Authorization: `Token ${token}` }
      })
      messages.value.push({
        role: 'bot',
        text: `- 만기 수령액(세전): ${res.data.maturity_amount.toLocaleString()}원\n- 적용 금리(최고우대금리): ${res.data.max_rate}%\n- 상품명: ${res.data.saving_name} (${res.data.save_trm}개월)`
      })
    } catch (e) {
      messages.value.push({ role: 'bot', text: '계산에 실패했습니다. 상품 옵션 또는 입력값을 확인해주세요.' })
    }
    step.value = 'idle'
    scrollToBottom()
    return
  }
  if (step.value === 'input_deposit_amount') {
    const amount = Number(inputAmount.value)
    if (!amount || isNaN(amount) || amount < 10000) {
      messages.value.push({ role: 'bot', text: '예치금액은 10,000원 이상 입력해야 합니다.' })
      inputAmount.value = ''
      scrollToBottom()
      return
    }
    messages.value.push({ role: 'user', text: `${amount}원` })
    // 예금 계산 API 호출
    try {
      const token = localStorage.getItem('token')
      const res = await apiChatbot.post('/calculate_deposit_maturity/', {
        deposit_name: selectedProduct.value,
        save_trm: inputMonth.value,
        amount: inputAmount.value
      }, {
        headers: { Authorization: `Token ${token}` }
      })
      messages.value.push({
        role: 'bot',
        text: `< ${res.data.deposit_name} (${res.data.save_trm}개월) >\n- 만기 수령액(세전): ${res.data.maturity_amount.toLocaleString()}원\n- 적용 금리(최고우대금리): ${res.data.max_rate}%`
      })
    } catch (e) {
      messages.value.push({ role: 'bot', text: '계산에 실패했습니다. 상품 옵션 또는 입력값을 확인해주세요.' })
    }
    step.value = 'idle'
    scrollToBottom()
    return
  }
}

const toggleChatbot = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) scrollToBottom()
}

const consumptionQuestions = [
  { question: "월급을 받으면 가장 먼저 하는 일은?", choices: ["저축한다", "쇼핑한다", "외식한다", "투자한다"] },
  { question: "가장 큰 지출 항목은?", choices: ["식비", "취미", "저축", "의류"] },
  { question: "지출 계획은 어떻게 세우나요?", choices: ["미리 계획", "필요할 때마다", "즉흥적으로", "가계부 작성"] },
  { question: "신용카드 사용 빈도는?", choices: ["자주 사용", "가끔 사용", "거의 안 씀", "항상 현금"] },
  { question: "저축 목표가 있나요?", choices: ["명확하다", "어렴풋하다", "없다", "매년 다르다"] },
  { question: "투자 경험이 있나요?", choices: ["있다", "없다", "관심 있다", "두렵다"] },
  { question: "비상금은 어떻게 관리하나요?", choices: ["항상 준비", "가끔 준비", "준비 안 함", "필요할 때만"] },
  { question: "가장 중요하게 생각하는 금융 목표는?", choices: ["내 집 마련", "여행", "노후 준비", "자기계발"] }
]
const consumptionStep = ref(0)
const consumptionAnswers = ref([])

const startConsumptionTest = () => {
  step.value = 'consumption'
  consumptionStep.value = 0
  consumptionAnswers.value = []
  messages.value.push({
    role: 'bot',
    text: consumptionQuestions[0].question,
    choices: consumptionQuestions[0].choices
  })
  scrollToBottom()
}

const closeConsumptionTest = () => {
  step.value = 'idle'
}

const selectConsumptionChoice = async (idx) => {
  // 답 저장
  consumptionAnswers.value.push(idx)
  // 사용자 답변 메시지 추가
  messages.value.push({
    role: 'user',
    text: consumptionQuestions[consumptionStep.value].choices[idx]
  })
  consumptionStep.value++
  // 다음 질문이 있으면
  if (consumptionStep.value < consumptionQuestions.length) {
    messages.value.push({
      role: 'bot',
      text: consumptionQuestions[consumptionStep.value].question,
      choices: consumptionQuestions[consumptionStep.value].choices
    })
  } else {
    // 결과 계산 및 결과 메시지 추가
    const result = calculateConsumptionResult(consumptionAnswers.value)
    messages.value.push({
      role: 'bot',
      text: `테스트 결과: ${result.type}\n${result.desc}`
    })

    // OpenAI 조언 요청
    try {
      const token = localStorage.getItem('token')
      const res = await apiChatbot.post('/ai_invest_advice/', {
        result_type: result.type,
        desc: result.desc
      }, {
        headers: { Authorization: `Token ${token}` }
      })
      messages.value.push({
        role: 'bot',
        text: res.data.advice
      })
    } catch (e) {
      messages.value.push({
        role: 'bot',
        text: 'AI 조언을 불러오지 못했습니다. 나중에 다시 시도해 주세요.'
      })
    }
    step.value = 'idle'
  }
  scrollToBottom()
}

function calculateConsumptionResult(answers) {
  // ...점수 계산 로직 (이전 답변 참고)...
  let saveScore = 0, spendScore = 0, investScore = 0, stableScore = 0, freeScore = 0
  if (answers[0] === 0) saveScore++
  if (answers[0] === 1 || answers[0] === 2) spendScore++
  if (answers[0] === 3) investScore++
  if (answers[1] === 2) saveScore++
  if (answers[1] === 1) spendScore++
  if (answers[1] === 0) spendScore++
  if (answers[1] === 3) spendScore++
  if (answers[2] === 0 || answers[2] === 3) saveScore++
  if (answers[2] === 2) freeScore++
  if (answers[3] === 3) saveScore++
  if (answers[3] === 0) spendScore++
  if (answers[4] === 0) saveScore++
  if (answers[4] === 2) freeScore++
  if (answers[5] === 0 || answers[5] === 2) investScore++
  if (answers[6] === 0) stableScore++
  if (answers[6] === 2) freeScore++
  if (answers[7] === 0 || answers[7] === 2) stableScore++
  if (answers[7] === 3) investScore++
  const scores = [
    { type: "절약형 소비자", score: saveScore, desc: "계획적이고 저축을 중시하는 타입입니다." },
    { type: "소비지향형 소비자", score: spendScore, desc: "소비와 경험을 즐기는 타입입니다." },
    { type: "투자지향형 소비자", score: investScore, desc: "투자와 자기계발에 관심이 많은 타입입니다." },
    { type: "안정추구형 소비자", score: stableScore, desc: "미래 대비와 안전을 중시하는 타입입니다." },
    { type: "즉흥형 소비자", score: freeScore, desc: "즉흥적이고 자유로운 소비를 선호하는 타입입니다." },
  ]
  scores.sort((a, b) => b.score - a.score)
  return scores[0]
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  right: 2rem;
  bottom: 2rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.chatbot-toggle {
  background: #006775;
  color: #fff;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  cursor: pointer;
  margin-bottom: 0.5rem;
  transition: background 0.2s;
}
.chatbot-toggle:hover {
  background: #009688;
}
.chatbot-box {
  width: 340px;
  max-height: 700px; /* 더 크게! */
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18);
  display: flex;
  flex-direction: column;
  overflow: auto;
  animation: fadeInUp 0.3s;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
.chatbot-header {
  background: #006775;
  color: #fff;
  padding: 1rem;
  font-weight: bold;
  text-align: center;
  font-size: 1.1rem;
}
.chatbot-messages {
  max-height: 350px; /* 원하는 높이로 조정 */
  min-height: 120px;
  overflow-y: auto;
  padding: 1rem;
  background: #f8fafb;
}
.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.7rem;
}
.message.bot {
  flex-direction: row;
}
.message.user {
  flex-direction: row-reverse;
}
.msg-text {
  background: #e0f7fa;
  color: #2ba4b4;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  margin: 0 0.5rem;
  max-width: 95%;
  word-break: break-all;
  font-size: 0.98rem;
  white-space: pre-line;
}
.message.user .msg-text {
  background: #f1f8e9;
  color: #333;
}
.chatbot-input-area {
  display: flex;
  gap: 0.5rem;
  padding: 0.8rem;
  border-top: 1px solid #e0e0e0;
  background: #fff;
  width: 100%;
  box-sizing: border-box;
}
.chatbot-input, .chatbot-select {
  flex: 1;
  border: 1px solid #b2dfdb;
  border-radius: 0.7rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  outline: none;
  min-width: 0;
}
.chatbot-btn, .calculator-btn {
  background: #335e64;
  color: #fff;
  border: none;
  border-radius: 0.7rem;
  padding: 0.5rem 1.1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  flex-shrink: 0;
  min-width: 80px;
}
.chatbot-btn:hover, .calculator-btn:hover {
  background: #009688;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.choices-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-left: 2.2rem; /* 말풍선과 아이콘 간격만큼 들여쓰기 */
  margin-top: -0.3rem;
  width: calc(100% - 2.2rem); /* 말풍선 너비와 맞춤 */
}

.choices-container .chatbot-btn {
  width: 100%;
  margin-bottom: 0.4rem;
  text-align: left;
  box-sizing: border-box;
}
.type-select-btns {
  margin-top: 0rem; /* 원하는 만큼 조절 (예: 1.2rem) */
  margin-bottom: 1.3rem;
}
</style>
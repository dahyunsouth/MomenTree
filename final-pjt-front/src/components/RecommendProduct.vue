<template>
  <div class="recommend-products">
    <div v-if="loading" class="loading">로딩 중...</div>
    <div v-else>
      <div class="product-section">
        <h2 class="section-title">
          <span class="icon">💰</span>
          추천 적금 상품
        </h2>
        <table v-if="savingProducts.length > 0">
          <thead>
            <tr>
              <th>상품명</th>
              <th>금융회사</th>
              <th>금리</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in savingProducts" :key="product.id">
              <td>
                <span
                  @click="selectedSavingName = product.fin_prdt_nm"
                  class="font-bold"
                  style="color: #007bff; text-decoration: underline; cursor: pointer;"
                >
                  {{ product.fin_prdt_nm }}
                </span>
              </td>
              <td>{{ product.kor_co_nm }}</td>
              <td>
                <span v-if="product.savingoption_set && product.savingoption_set.length > 0">
                  {{ getBestRate(product.savingoption_set, desirePeriod) }}%
                </span>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else class="no-products">추천할 적금 상품이 없습니다.</p>
      </div>

      <div class="product-section">
        <h2 class="section-title">
          <span class="icon">💸</span>
          추천 예금 상품
        </h2>
        <table v-if="depositProducts.length > 0">
          <thead>
            <tr>
              <th>상품명</th>
              <th>금융회사</th>
              <th>금리</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in depositProducts" :key="product.id">
              <td>
                <span
                  @click="selectedDepositName = product.fin_prdt_nm"
                  class="font-bold"
                  style="color: #007bff; text-decoration: underline; cursor: pointer;"
                >
                  {{ product.fin_prdt_nm }}
                </span>
              </td>
              <td>{{ product.kor_co_nm }}</td>
              <td>
                <span v-if="product.depositoption_set && product.depositoption_set.length > 0">
                  {{ getBestRate(product.depositoption_set, desirePeriod) }}%
                </span>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else class="no-products">추천할 예금 상품이 없습니다.</p>
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <!-- 적금 상세 -->
    <div v-if="selectedSavingName" class="modal-card" @click.self="selectedSavingName = null">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">상품 상세 정보</div>
          <button @click="selectedSavingName = null" class="close-btn">&times;</button>
        </div>
        <SavingDetail :saving_name="selectedSavingName" />
      </div>
    </div>
    <!-- 예금 상세 -->
    <div v-if="selectedDepositName" class="modal-card" @click.self="selectedDepositName = null">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">상품 상세 정보</div>
          <button @click="selectedDepositName = null" class="close-btn">&times;</button>
        </div>
        <DepositDetail :deposit_name="selectedDepositName" />
      </div>
    </div>
  </div>
</template>

<script>
import SavingDetail from './SavingDetail.vue'
import DepositDetail from './DepositDetail.vue'

export default {
  name: 'RecommendProducts',
  data() {
    return {
      savingProducts: [],
      depositProducts: [],
      loading: true,
      error: null,
      desirePeriod: null,
      selectedSavingName: null,
      selectedDepositName: null,
    };
  },
  mounted() {
    fetch('http://localhost:8000/accounts/profile/', {
      headers: { 'Authorization': `Token ${localStorage.getItem('token')}` }
    })
      .then(res => res.json())
      .then(data => {
        console.log('user profile data:', data);
        this.desirePeriod = data.user.desire_period;
        console.log('desirePeriod:', this.desirePeriod);
      });

    // 추천 상품 가져오기 (기존 코드)
    fetch('http://localhost:8000/api/recommend/', {
      headers: { 'Authorization': `Token ${localStorage.getItem('token')}` }
    })
      .then(async res => {
        const text = await res.text();
        if (!res.ok) throw new Error('로그인 후 이용해 주세요.');
        return JSON.parse(text);
      })
      .then(data => {
        this.savingProducts = data.saving_products;
        this.depositProducts = data.deposit_products;
        this.loading = false;
      })
      .catch(err => {
        this.error = err.message;
        this.loading = false;
      });
  },
  methods: {
    getBestRate(optionSet, desirePeriod) {
      if (!optionSet || !Array.isArray(optionSet) || !desirePeriod) return '-';
      // 희망 기간 이하 옵션만 필터링
      const filtered = optionSet.filter(opt => Number(opt.save_trm) <= Number(desirePeriod));
      if (filtered.length === 0) return '-';
      // save_trm이 가장 큰 옵션 찾기
      const best = filtered.reduce((a, b) => Number(a.save_trm) > Number(b.save_trm) ? a : b);
      // 우대금리(intr_rate2)가 더 높으면 그걸, 아니면 기본금리(intr_rate)
      return best.intr_rate2 && Number(best.intr_rate2) > Number(best.intr_rate)
        ? best.intr_rate2
        : best.intr_rate;
    },
  },
  components: {
    SavingDetail,
    DepositDetail
  }
};
</script>

<style scoped>
.recommend-products {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.product-section {
  margin-bottom: 30px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  padding: 14px 5px;
  font-size: 1.7rem;
  font-weight: bold;
  margin-bottom: 0;
  background: transparent;
}

.section-title .icon {
  margin-right: 10px;
  font-size: 1.7rem;
}

.product-list {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}

.product-list-item {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,191,174,0.10);
  padding: 16px;
  position: relative;
  transition: transform 0.18s, box-shadow 0.18s;
}

.product-list-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0,191,174,0.18);
}

.list-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #00796b;
  margin: 10px 0;
  display: flex;
  align-items: center;
}

.list-badge {
  background: linear-gradient(135deg, #00bfae 0%, #00e6c3 100%);
  color: #fff;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.9rem;
  margin-right: 8px;
}

.list-company {
  font-size: 0.9rem;
  color: #888;
}

.list-rate {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #00bfae 60%, #00e6c3 100%);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 1px 6px rgba(0,191,174,0.07);
}

.card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 10px;
}

.product-card {
  flex: 1 1 calc(33.333% - 10px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,191,174,0.10);
  padding: 16px;
  position: relative;
  transition: transform 0.18s, box-shadow 0.18s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0,191,174,0.18);
}

.card-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #00796b;
  margin: 10px 0;
}

.card-company {
  font-size: 0.9rem;
  color: #888;
}

.card-rate {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #00bfae 60%, #00e6c3 100%);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 1px 6px rgba(0,191,174,0.07);
}

.top3-row {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.top3-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,191,174,0.10);
  padding: 16px;
  position: relative;
  transition: transform 0.18s, box-shadow 0.18s;
}

.top3-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0,191,174,0.18);
}

.top3-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  color: #fff;
  background: linear-gradient(135deg, #00bfae 0%, #00e6c3 100%);
  box-shadow: 0 2px 8px rgba(0,191,174,0.10);
}

.top3-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #00796b;
  margin: 10px 0;
}

.top3-company {
  font-size: 0.9rem;
  color: #888;
}

.top3-rate {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #00bfae 60%, #00e6c3 100%);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 1px 6px rgba(0,191,174,0.07);
}

.bottom-row {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.bottom-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,191,174,0.10);
  padding: 16px;
  position: relative;
  transition: transform 0.18s, box-shadow 0.18s;
}

.bottom-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0,191,174,0.18);
}

.bottom-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  color: #fff;
  background: linear-gradient(135deg, #cd7f32 0%, #f7e6d2 100%);
  box-shadow: 0 2px 8px rgba(0,191,174,0.10);
}

.bottom-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #00796b;
  margin: 10px 0;
}

.bottom-company {
  font-size: 0.9rem;
  color: #888;
}

.bottom-rate {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #00bfae 60%, #00e6c3 100%);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 1px 6px rgba(0,191,174,0.07);
  margin-top: auto;
}

.ranked-product-list {
  list-style: none;
  padding: 0;
  margin: 24px 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ranked-product-item {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 20px rgba(0,191,174,0.10);
  padding: 22px 28px;
  gap: 22px;
  transition: box-shadow 0.18s, transform 0.18s;
  position: relative;
  border: 1.5px solid #e0f7fa;
}

.ranked-product-item:hover {
  box-shadow: 0 10px 32px rgba(0,191,174,0.18);
  transform: translateY(-3px) scale(1.02);
  border-color: #00bfae;
}

.rank-badge {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 18px;
  background: #e0f7fa;
  color: #00bfae;
  box-shadow: 0 2px 8px rgba(0,191,174,0.10);
  flex-shrink: 0;
  border: 2.5px solid #fff;
}
.rank-1 { background: linear-gradient(135deg, #ffd700 70%, #fffbe7 100%); color: #bfa100; }
.rank-2 { background: linear-gradient(135deg, #b0c4de 70%, #f4f8fc 100%); color: #5a6e8c; }
.rank-3 { background: linear-gradient(135deg, #cd7f32 70%, #f7e6d2 100%); color: #a05a2c; }

.ranked-product-info {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ranked-title {
  font-size: 1.18rem;
  font-weight: bold;
  color: #00796b;
  letter-spacing: 0.5px;
}

.ranked-company {
  font-size: 1rem;
  color: #888;
}

.ranked-rate {
  flex: 1;
  text-align: right;
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #00bfae 60%, #00e6c3 100%);
  padding: 8px 22px;
  border-radius: 20px;
  box-shadow: 0 1px 6px rgba(0,191,174,0.07);
  margin-left: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 10px;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #eee;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

tbody tr {
  height: 72px;  /* 행 높이 설정 */
}

/* 각 열의 너비를 고정 */
th:nth-child(1), td:nth-child(1) {
  width: 45%;  /* 상품명 */
}

th:nth-child(2), td:nth-child(2) {
  width: 30%;  /* 금융회사 */
}

th:nth-child(3), td:nth-child(3) {
  width: 25%;  /* 금리 */
  text-align: left;  /* 금리는 왼쪽 정렬 */
  padding-right: 32px;  /* 오른쪽 여백 추가 */
}

thead {
  background-color: #f8f9fa;
}

thead th {
  font-weight: 600;
  color: #333;
}

/* 마지막 행의 셀들에 대한 스타일 */
tbody tr:last-child td {
  border-bottom: none;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.no-products {
  text-align: center;
  padding: 20px;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.error-message {
  color: #dc3545;
  padding: 10px;
  margin-top: 10px;
  background-color: #fff3f3;
  border-radius: 4px;
  text-align: center;
}

.product-slider {
  margin: 24px 0 0 0;
}
.slider-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 20px rgba(0,191,174,0.10);
  padding: 32px 18px 24px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  min-width: 220px;
  max-width: 260px;
  margin: 0 auto;
  transition: box-shadow 0.18s, transform 0.18s;
  border: 2.5px solid #e0f7fa;
}
.slider-card:hover {
  box-shadow: 0 12px 36px rgba(0,191,174,0.18);
  transform: translateY(-4px) scale(1.04);
}
.slider-badge {
  position: absolute;
  top: -22px;
  left: 50%;
  transform: translateX(-50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,191,174,0.10);
  border: 3px solid #fff;
  background: #e0f7fa;
  color: #00bfae;
  z-index: 2;
}
.slider-card.rank-1 .slider-badge { background: linear-gradient(135deg, #ffd700 70%, #fffbe7 100%); color: #bfa100; }
.slider-card.rank-2 .slider-badge { background: linear-gradient(135deg, #b0c4de 70%, #f4f8fc 100%); color: #5a6e8c; }
.slider-card.rank-3 .slider-badge { background: linear-gradient(135deg, #cd7f32 70%, #f7e6d2 100%); color: #a05a2c; }

.slider-title {
  margin-top: 38px;
  font-size: 1.18rem;
  font-weight: bold;
  color: #00796b;
  text-align: center;
}
.slider-company {
  font-size: 1rem;
  color: #888;
  margin: 6px 0 12px 0;
  text-align: center;
}
.slider-rate {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #00bfae 60%, #00e6c3 100%);
  padding: 8px 22px;
  border-radius: 20px;
  margin-top: auto;
}

.modal-card {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-y: auto;
  padding: 20px;
}

.modal-content {
  background-color: #fff;
  padding: 32px 24px;
  border-radius: 16px;
  max-width: 700px;
  width: 100%;
  box-shadow: 0 4px 32px rgba(0,0,0,0.18);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: bold;
}

.close-btn {
  position: static;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  margin: 0;
  line-height: 1;
}
</style>

<template>
  <div class="product-list">
    <div class="filters">
      <div class="product-type">
        <button :class="{ active: productType === 'deposit' }" @click="productType = 'deposit'">예금</button>
        <button :class="{ active: productType === 'saving' }" @click="productType = 'saving'">적금</button>
      </div>
      
      <div class="filter-options">
        <select v-model="selectedBank">
          <option value="">은행 선택</option>
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
        
        <select v-model="selectedTerm">
          <option value="">예치기간 선택</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
        
        <button @click="applyFilters">확인</button>
      </div>
    </div>

    <div class="products" v-if="filteredProducts.length">
      <table>
        <thead>
          <tr>
            <th>공시 제출일</th>
            <th>금융회사명</th>
            <th>상품명</th>
            <th>가입기간</th>
            <th>금리</th>
            <th>세부사항</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
            <td>{{ product.dcls_month }}</td>
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.fin_prdt_nm }}</td>
            <td>
              <span v-for="option in product.options" :key="option.save_trm">
                {{ option.save_trm }}개월: {{ option.intr_rate }}%
                <br>
              </span>
            </td>
            <td>{{ product.mtrt_int }}</td>
            <td>
              <button @click="showDetails(product)">상세보기</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-products">
      조건에 맞는 상품이 없습니다.
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProductList',
  data() {
    return {
      productType: 'deposit',
      products: [],
      banks: [],
      selectedBank: '',
      selectedTerm: '',
      filteredProducts: []
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const endpoint = this.productType === 'deposit' ? 'deposit' : 'saving'
        const response = await axios.get(`http://127.0.0.1:8000/products/${endpoint}/`)
        this.products = response.data
        this.updateBanks()
        this.applyFilters()
      } catch (error) {
        console.error('상품 데이터를 불러오는데 실패했습니다:', error)
      }
    },
    updateBanks() {
      this.banks = [...new Set(this.products.map(product => product.kor_co_nm))]
    },
    applyFilters() {
      let filtered = [...this.products]
      
      if (this.selectedBank) {
        filtered = filtered.filter(product => product.kor_co_nm === this.selectedBank)
      }
      
      if (this.selectedTerm) {
        filtered = filtered.filter(product => {
          return product.options.some(option => option.save_trm === parseInt(this.selectedTerm))
        })
      }
      
      this.filteredProducts = filtered
    },
    showDetails(product) {
      // 상세 정보 표시 로직 구현
      console.log('상품 상세 정보:', product)
    }
  },
  watch: {
    productType() {
      this.fetchProducts()
    }
  },
  created() {
    this.fetchProducts()
  }
}
</script>

<style scoped>
.product-list {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
}

.product-type {
  margin-bottom: 15px;
}

.product-type button {
  padding: 8px 16px;
  margin-right: 10px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
}

.product-type button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.filter-options {
  display: flex;
  gap: 10px;
  align-items: center;
}

select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.no-products {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style> 
<template>
  <div class="min-h-screen px-4 py-8" style="overflow-y: auto;">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-2xl font-bold mb-6">🏦 주변 은행 찾기 및 길찾기 🏦</h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- 왼쪽 영역 -->
        <div class="lg:col-span-4 space-y-6">
          <!-- 검색 박스 -->
          <div class="bg-white/50 rounded-3xl shadow-lg p-6">
            <h3 class="text-lg font-semibold mb-4">은행 검색</h3>
            <div class="space-y-4">
              <!-- 시/도 선택 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">시/도 *</label>
                <div class="relative">
                  <select
                    v-model="selectedSido"
                    @change="onSidoChange"
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent appearance-none bg-white cursor-pointer"
                    required
                  >
                    <option value="" disabled selected>선택해주세요</option>
                    <option v-for="region in mapInfo" :key="region.name" :value="region.name">{{ region.name }}</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                    <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <!-- 시/군/구 선택 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">시/군/구 *</label>
                <div class="relative">
                  <select
                    v-model="selectedSigungu"
                    @change="onSigunguChange"
                    :disabled="!selectedSido"
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent appearance-none bg-white cursor-pointer disabled:bg-gray-100 disabled:cursor-not-allowed"
                    required
                  >
                    <option value="" disabled selected>선택해주세요</option>
                    <option v-for="sigungu in sigunguList" :key="sigungu" :value="sigungu">{{ sigungu }}</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                    <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <!-- 은행 선택 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">은행 *</label>
                <div class="relative">
                  <select
                    v-model="selectedBank"
                    :disabled="!selectedSigungu"
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent appearance-none bg-white cursor-pointer disabled:bg-gray-100 disabled:cursor-not-allowed"
                    required
                  >
                    <option value="" disabled selected>선택해주세요</option>
                    <option v-for="bank in bankInfo" :key="bank" :value="bank">{{ bank }}</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                    <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <!-- 검색하기 버튼 -->
              <button
                @click="displayMarkers"
                :disabled="!selectedBank"
                class="w-full bg-[#006775] text-white py-3 px-4 rounded-lg hover:bg-[#005766] transition-colors mt-4 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                은행 검색하기
              </button>
            </div>
          </div>

          <!-- 출발지 검색 박스 -->
          <div class="bg-white/50 rounded-3xl shadow-lg p-6">
            <h3 class="text-lg font-semibold mb-4">출발지 설정</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">출발지 검색</label>
                <input
                  type="text"
                  v-model="startLocationQuery"
                  @keyup.enter="searchStartLocation"
                  placeholder="출발지를 입력하세요 (예: 강남역)"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#006775] focus:border-transparent"
                />
              </div>
              
              <!-- 검색 결과 목록 -->
              <div v-if="startLocationResults.length > 0" class="bg-gray-50 rounded-lg max-h-40 overflow-y-auto">
                <ul>
                  <li
                    v-for="place in startLocationResults"
                    :key="place.id"
                    @click="selectStartLocation(place)"
                    class="px-4 py-2 cursor-pointer hover:bg-gray-200"
                  >
                    <p class="font-medium">{{ place.place_name }}</p>
                    <p class="text-sm text-gray-500">{{ place.address_name }}</p>
                  </li>
                </ul>
              </div>

              <!-- 선택된 출발지 정보 -->
              <div v-if="selectedStartLocation" class="bg-white rounded-lg shadow-md p-4">
                <h4 class="text-md font-semibold mb-2">선택된 출발지:</h4>
                <p class="font-medium">{{ selectedStartLocation.place_name }}</p>
                <p class="text-sm text-gray-500">{{ selectedStartLocation.address_name }}</p>
                <button @click="clearStartLocation" class="mt-2 text-sm text-red-600 hover:underline">
                  선택 취소
                </button>
              </div>

              <!-- 이동 수단 선택 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">이동 수단 선택</label>
                <div class="flex space-x-4">
                  <label class="inline-flex items-center">
                    <input
                      type="radio"
                      class="form-radio text-[#006775] focus:ring-[#006775]"
                      name="travelMode"
                      value="car"
                      v-model="selectedTravelMode"
                      checked
                    />
                    <span class="ml-2 text-gray-700">자동차</span>
                  </label>
                  <label class="inline-flex items-center">
                    <input type="radio" class="form-radio text-[#006775] focus:ring-[#006775]" name="travelMode" value="walk" v-model="selectedTravelMode" disabled />
                    <span class="ml-2 text-gray-700">도보 (미지원)</span>
                  </label>
                </div>
                <p class="mt-2 text-sm text-gray-500">현재는 자동차 길찾기만 지원됩니다.</p>
              </div>

              <!-- 길찾기 버튼 -->
              <button
                @click="findRoute"
                :disabled="!selectedStartLocation || !selectedPlace"
                class="w-full bg-[#006775] text-white py-3 px-4 rounded-lg hover:bg-[#005766] transition-colors mt-4 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                길찾기
              </button>
            </div>
          </div>

          <!-- 은행 정보 박스 -->
          <div v-if="selectedPlace" class="bg-white/50 rounded-3xl shadow-lg p-6">
            <h3 class="text-lg font-semibold mb-4">선택된 은행 정보 (도착지)</h3>
            <div class="space-y-3">
              <div>
                <p class="text-sm text-gray-500">지점명</p>
                <p class="font-medium">{{ selectedPlace.place_name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">주소</p>
                <p class="font-medium">{{ selectedPlace.address_name }}</p>
              </div>
              <div v-if="selectedPlace.phone">
                <p class="text-sm text-gray-500">전화번호</p>
                <p class="font-medium">{{ selectedPlace.phone }}</p>
              </div>
              <div v-if="selectedPlace.road_address_name">
                <p class="text-sm text-gray-500">도로명 주소</p>
                <p class="font-medium">{{ selectedPlace.road_address_name }}</p>
              </div>
              <div v-if="travelTime">
                <p class="text-sm text-gray-500">예상 소요 시간</p>
                <p class="font-medium text-lg text-[#006775]">{{ travelTime }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 오른쪽 지도 영역 -->
        <div class="lg:col-span-8 bg-white rounded-3xl shadow-lg">
          <div id="map" class="w-full h-full rounded-3xl" style="position: relative;">
            <div v-if="!mapLoaded" class="flex items-center justify-center h-full text-gray-500">
              지도를 불러오는 중입니다...
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 예상 소요 시간 팝업 -->
    <div v-if="showTimePopup" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl p-8 max-w-sm w-full text-center">
        <h3 class="text-2xl font-bold mb-4 text-[#006775]">예상 소요 시간</h3>
        <p v-if="travelTime" class="text-4xl font-extrabold text-[#006775] mb-6">{{ travelTime }}</p>
        <p v-else class="text-lg text-gray-700 mb-6">소요 시간 정보를 가져오지 못했습니다.</p>
        <button
          @click="closeTimePopup"
          class="bg-gray-300 text-gray-800 py-2 px-6 rounded-lg hover:bg-gray-400 transition-colors"
        >
          닫기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import config from '@/config/apikey.js'
import mapData from '@/data/data.json'

// 반응형 상태 정의
const map = ref(null)
const ps = ref(null)
const markers = ref([])
const destInfo = ref(null)
const mapLoaded = ref(false)

const mapInfo = ref(mapData.mapInfo)
const bankInfo = ref(mapData.bankInfo)
const sigunguList = ref([])
const bankList = ref([])

const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const selectedPlace = ref(null)
const showMessage = ref(false)
const startLocationQuery = ref('')
const startLocationResults = ref([])
const selectedStartLocation = ref(null)
const routePolyline = ref(null)
const startMarker = ref(null)
const endMarker = ref(null)
const travelTime = ref(null)
const selectedTravelMode = ref('car')
const timeOverlay = ref(null)
const showTimePopup = ref(false)

// 지도 초기화
const initMap = () => {
  try {
    const container = document.getElementById('map')
    if (!container) {
      console.error('지도 컨테이너를 찾을 수 없습니다')
      return
    }
    
    const options = {
      center: new window.kakao.maps.LatLng(33.450701, 126.570667), // 초기 중심 좌표
      level: 3
    }
    
    map.value = new window.kakao.maps.Map(container, options)
    ps.value = new window.kakao.maps.services.Places()
    destInfo.value = new window.kakao.maps.InfoWindow({ removable: true })
    mapLoaded.value = true
  } catch (error) {
    console.error('지도 초기화 중 오류 발생:', error)
  }
}

// 시/도 선택 변경 시
const onSidoChange = () => {
  selectedSigungu.value = ''
  sigunguList.value = []
  bankList.value = []
  selectedBank.value = ''
  selectedPlace.value = null
  showMessage.value = false
  const region = mapInfo.value.find(x => x.name === selectedSido.value)
  if (!region) return
  sigunguList.value = [...region.countries]
}

// 시/군/구 선택 변경 시
const onSigunguChange = () => {
  selectedBank.value = ''
  bankList.value = selectedSigungu.value ? [...bankInfo.value] : []
  selectedPlace.value = null
  showMessage.value = false
}

// 마커 초기화
const clearMarkers = () => {
  markers.value.forEach(obj => obj.marker.setMap(null))
  markers.value = []
}

// 정보창 초기화
const clearInfos = () => {
  if (destInfo.value) destInfo.value.close()
  selectedPlace.value = null
}

// 마커 표시
const displayMarkers = () => {
  if (!ps.value) {
    alert('지도가 아직 초기화되지 않았습니다.');
    return;
  }
  
  try {
    showMessage.value = true
    clearMarkers()
    clearInfos()
    clearRouteAndMarkers()

    const query = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`;
    ps.value.keywordSearch(query, (places, status) => {
      if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
        alert('검색 결과가 없습니다.');
        return;
      }
      if (status !== window.kakao.maps.services.Status.OK) {
        alert('검색 중 오류가 발생했습니다.');
        return;
      }
      
      const bounds = new window.kakao.maps.LatLngBounds();
      places.forEach(p => {
        const pos = new window.kakao.maps.LatLng(p.y, p.x);
        const m = new window.kakao.maps.Marker({ map: map.value, position: pos });
        markers.value.push({ marker: m, place: p });
        bounds.extend(pos);
        window.kakao.maps.event.addListener(m, 'click', () => {
          clearInfos();
          selectedPlace.value = p;
        });
      });
      map.value.setBounds(bounds);
    });
  } catch (error) {
    console.error('마커 표시 중 오류 발생:', error);
    alert('지도 표시 중 오류가 발생했습니다.');
  }
}

// 출발지 검색
const searchStartLocation = () => {
  if (!ps.value || !startLocationQuery.value.trim()) {
    startLocationResults.value = []
    return
  }

  // 기존 검색 결과 및 선택된 출발지 초기화
  startLocationResults.value = []
  // selectedStartLocation.value = null; // 선택된 출발지는 검색 시 유지

  ps.value.keywordSearch(startLocationQuery.value.trim(), (places, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      startLocationResults.value = places
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      startLocationResults.value = []
      alert('검색 결과가 없습니다.')
    } else {
      startLocationResults.value = []
      alert('출발지 검색 중 오류가 발생했습니다.')
    }
  })
}

// 출발지 선택
const selectStartLocation = (place) => {
  selectedStartLocation.value = place;
  startLocationResults.value = []; // 검색 결과 목록 숨김
  startLocationQuery.value = place.place_name; // 검색창에 선택된 장소 이름 표시
  // 선택된 출발지에 마커 표시 및 지도 relayout 호출 (DOM 업데이트 후)
  nextTick(() => {
    // TODO: 선택된 출발지에 마커 표시 로직 추가 (필요하다면)
    if (map.value) map.value.relayout();
  });
}

// 출발지 취소
const clearStartLocation = () => {
  // 여기에 출발지 취소 로직을 구현해야 합니다.
  selectedStartLocation.value = null;
  startLocationQuery.value = '';
  startLocationResults.value = [];
  // TODO: 출발지 마커 제거 로직 추가
  // TODO: 길찾기 경로 및 마커 제거 로직 추가
  clearRouteAndMarkers();
  // 지도 relayout 호출 (DOM 업데이트 후)
  nextTick(() => {
    if (map.value) map.value.relayout();
  });
}

// 경로 및 마커 초기화
const clearRouteAndMarkers = () => {
  // 경로선 제거
  if (routePolyline.value) {
    routePolyline.value.setMap(null);
    routePolyline.value = null;
  }
  
  // 출발지 마커 제거
  if (startMarker.value) {
    startMarker.value.setMap(null);
    startMarker.value = null;
  }
  
  // 도착지 마커 제거
  if (endMarker.value) {
    endMarker.value.setMap(null);
    endMarker.value = null;
  }

  // 시간 오버레이 제거
  if (timeOverlay.value) {
    timeOverlay.value.setMap(null);
    timeOverlay.value = null;
  }

  // 소요 시간 초기화
  travelTime.value = null;
}

// 마커 이미지 생성
const createMarkerImage = (type) => {
  const imageSrc = type === '출발' ? 
    'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/red_b.png' : 
    'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/blue_b.png';
  return new window.kakao.maps.MarkerImage(
    imageSrc,
    new window.kakao.maps.Size(50, 45),
    { offset: new window.kakao.maps.Point(15, 43) }
  );
}

// 길찾기
const findRoute = async () => {
  if (!selectedStartLocation.value || !selectedPlace.value) {
    alert('출발지와 도착지를 모두 선택해주세요.');
    return;
  }

  // 기존 경로, 마커, 오버레이 초기화
  clearRouteAndMarkers();
  travelTime.value = null; // 소요 시간 초기화
  showTimePopup.value = false; // 팝업 숨김

  // 길찾기 시작 시에는 모든 은행 마커 숨기기
   markers.value.forEach(obj => {
    if (obj.place !== selectedPlace.value) {
      obj.marker.setMap(null);
    }
  });

  const origin = `${selectedStartLocation.value.x},${selectedStartLocation.value.y}`;
  const destination = `${selectedPlace.value.x},${selectedPlace.value.y}`;
  const restApiKey = config.REST_API_KEY; // apikey.js에서 REST API 키 가져오기

  const apiUrl = `https://apis-navi.kakaomobility.com/v1/directions?origin=${origin}&destination=${destination}`;

  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Authorization': `KakaoAK ${restApiKey}`,
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (data.routes && data.routes.length > 0) {
      const route = data.routes[0];
      const sections = route.sections;
      const linePath = [];

      sections.forEach(section => {
        section.roads.forEach(road => {
          road.vertexes.forEach((vertex, index) => {
            if (index % 2 === 0) {
              linePath.push(new window.kakao.maps.LatLng(road.vertexes[index + 1], vertex));
            }
          });
        });
      });

      // 경로 선 그리기
      const polyline = new window.kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 5,
        strokeColor: '#FF0000',
        strokeOpacity: 0.7,
        strokeStyle: 'solid'
      });

      polyline.setMap(map.value);
      routePolyline.value = polyline;

      // 출발지 마커 표시
      const startPos = new window.kakao.maps.LatLng(
        parseFloat(selectedStartLocation.value.y),
        parseFloat(selectedStartLocation.value.x)
      );
      const startImage = createMarkerImage('출발');

      // 도착지 마커 표시
      const endPos = new window.kakao.maps.LatLng(
        parseFloat(selectedPlace.value.y),
        parseFloat(selectedPlace.value.x)
      );
      const endImage = createMarkerImage('도착');

      const startM = new window.kakao.maps.Marker({
        position: startPos,
        map: map.value,
        image: startImage
      });
      startMarker.value = startM;

      const endM = new window.kakao.maps.Marker({
        position: endPos,
        map: map.value,
        image: endImage
      });
      endMarker.value = endM;

      // 지도 범위 재설정
      const bounds = new window.kakao.maps.LatLngBounds();
      bounds.extend(startPos);
      bounds.extend(endPos);
      linePath.forEach(pos => bounds.extend(pos));
      map.value.setBounds(bounds);

      // 소요 시간 계산 및 표시
      const duration = route.summary.duration;
      const hours = Math.floor(duration / 3600);
      const minutes = Math.floor((duration % 3600) / 60);
      travelTime.value = `${hours > 0 ? `${hours}시간 ` : ''}${minutes}분`;

      // 소요 시간 팝업 표시
      showTimePopup.value = true;
    }
  } catch (error) {
    console.error('길찾기 중 오류 발생:', error);
    alert('길찾기 중 오류가 발생했습니다.');
  }
}

// 소요 시간 팝업 닫기
const closeTimePopup = () => {
  showTimePopup.value = false;
}

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  // window.kakao가 로드될 때까지 대기
  const initializeMap = () => {
    if (window.kakao && window.kakao.maps) {
      initMap()
    } else {
      setTimeout(initializeMap, 100)
    }
  }
  
  initializeMap()
})
</script>

<style scoped>
select {
  /* Firefox */
  -moz-appearance: none;
  /* Safari and Chrome */
  -webkit-appearance: none;
  appearance: none;
}

/* 드롭다운 메뉴가 아래로 펼쳐지도록 설정 */
select {
  position: relative;
}

/* 드롭다운 메뉴의 위치와 방향 설정 */
select:not([multiple]) {
  background-color: white;
}

/* 드롭다운 옵션 스타일링 */
select option {
  position: absolute;
  background-color: white;
  color: black;
  padding: 8px;
}

/* Firefox에서 드롭다운 방향 설정 */
@-moz-document url-prefix() {
  select {
    text-indent: 0;
  }
  select option {
    direction: ltr;
    position: relative !important;
  }
}

/* Chrome/Safari에서 드롭다운 방향 설정 */
@media screen and (-webkit-min-device-pixel-ratio:0) {
  select {
    text-indent: 0;
  }
  select option {
    direction: ltr;
    position: relative !important;
  }
}

.place-info {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 지도 컨테이너 높이 설정 */
#map {
  min-height: 600px;
}
</style>
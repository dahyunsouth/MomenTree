import random
import requests
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pjt_back.settings")
django.setup()

first_name_samples = "김이박최정강조윤장임신유한오서전황원문양손배백남"
middle_name_samples = "민효세경서예지도하주윤채현지진승연다재"
last_name_samples = "준윤우원호후서연아은진수혁영경환인희유현"


def random_name():
    result = ""
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result + str(random.randint(1, 100))

# 현재 API 에 들어있는 금융 상품 코드 리스트 저장
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'

API_KEY='075aba31f295dc17f85b416dfabc2969'

financial_products = []

params = {
  'auth': API_KEY,
  # 금융회사 코드 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
  'topFinGrpNo': '020000',
  'pageNo': 1
}

# 정기예금 목록 저장
response = requests.get(DP_URL, params=params).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    financial_products.append(product['fin_prdt_cd'])

# 적금 목록 저장
response = requests.get(SP_URL, params=params).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    financial_products.append(product['fin_prdt_cd'])

dict_keys = ['username', 'gender', 'financial_products', 'age', 'money', 'salary']

# json 파일 만들기
import json
from collections import OrderedDict

file = OrderedDict()

username_list = []
N = 2500
i = 0

while i < N:
    rn = random_name()
    if rn in username_list:
        continue
    
    username_list.append(rn)
    i += 1

    
    
# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = 'financial_products/fixtures/financial_products/user_data.json'
with open(save_dir, 'w', encoding="utf-8") as f:
    f.write('[')
    
    for i in range(N):
        # 랜덤한 데이터를 삽입
        file["model"] = "accounts.User"
        file["pk"] = i+1
        file["fields"] = {
            'username': 'testuser' + str(i+1),  # 유저 이름 랜덤 생성
            'nickname': username_list[i],
            # 랜덤한 0~5개의 상품을 가입하도록 삽입됨
            # 'financial_products': ','.join([random.choice(financial_products) for _ in range(random.randint(0, 5))]), # 금융 상품 리스트
            'age': random.randint(18, 99),  # 나이
            'profile_img': 'images/default_profile.png',
            'salary': random.randrange(30, 150000), # 연봉
            'wealth': random.randrange(10, 100000), # 자산
            'password': make_password("password12341234"),
            'desire_period': random.choice([6, 12, 24, 36]),
            'monthly_deposit': random.randrange(1, 1000),
        }

        json.dump(file, f, ensure_ascii=False, indent="\t")
        if i != N-1:
            f.write(',')
    f.write(']')
    f.close()

print(f'데이터 생성 완료 / 저장 위치: {save_dir}')
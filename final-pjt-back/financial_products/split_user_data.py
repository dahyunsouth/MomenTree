import json

# 1. 기존 user_data.json 파일 읽기
with open('financial_products/fixtures/financial_products/user_data.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# 2. 분할할 파일 개수 및 크기 계산
num_files = 5
users_per_file = len(users) // num_files

# 3. 파일로 나누어 저장
for i in range(num_files):
    start = i * users_per_file
    # 마지막 파일은 남은 모든 사용자 포함
    end = (i + 1) * users_per_file if i < num_files - 1 else len(users)
    chunk = users[start:end]
    with open(f'financial_products/fixtures/financial_products/user_data_part_{i+1}.json', 'w', encoding='utf-8') as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)

print("분할 완료!")
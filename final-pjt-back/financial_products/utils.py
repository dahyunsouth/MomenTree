import openai
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()  # 같은 폴더의 .env 파일을 자동으로 로드

def generate_analysis_prompt(answers):
    prompt = f"""
    사용자의 소비 성향 테스트 결과:
    1. {answers[0]}
    2. {answers[1]}
    3. {answers[2]}
    4. {answers[3]}
    5. {answers[4]}
    6. {answers[5]}
    7. {answers[6]}
    8. {answers[7]}
    
    위 결과를 바탕으로 소비 유형, 강점/약점, 맞춤 자산관리 전략을 5줄 이내로 요약해 주세요.
    """
    return prompt

def analyze_with_openai(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print("OPENAI_API_KEY:", repr(openai.api_key))  # 실제 값 확인
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 예리하고 분석적인 금융 자문 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

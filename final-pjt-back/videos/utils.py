import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import openai

print("\n=== 환경 설정 로드 ===")
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("OpenAI API 키가 로드됨")
    openai.api_key = api_key
else:
    print("경고: OpenAI API 키를 찾을 수 없음!")

def get_video_id_from_url(url):
    """YouTube URL에서 비디오 ID를 추출합니다."""
    print(f"\n1. URL 처리 시작 - 입력된 URL: {url}")  # 입력 URL 로깅
    # URL에 'youtube.com'이나 'youtu.be'가 없다면 이미 ID로 간주
    if 'youtube.com' not in url and 'youtu.be' not in url:
        print(f"   -> 이미 ID 형식으로 간주: {url}")  # ID 추출 로깅
        return url
    
    if 'youtu.be' in url:
        result = url.split('/')[-1]
    elif 'youtube.com' in url:
        result = url.split('v=')[1].split('&')[0]
    else:
        result = url
    print(f"   -> 추출된 비디오 ID: {result}")  # 최종 ID 로깅
    return result

def get_video_transcript(video_id):
    """YouTube 비디오의 자막을 가져옵니다."""
    print(f"\n2. 자막 추출 시작 - 비디오 ID: {video_id}")  # 자막 추출 시작 로깅
    try:
        # 먼저 일반 자막 시도
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
            print("   -> 한국어 자막 찾음")
        except:
            # 한국어 자막이 없으면 영어 자막 시도
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                print("   -> 영어 자막 찾음")
            except:
                # 일반 자막이 없으면 자동 생성 자막 시도
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'], preserve_formatting=True)
                    print("   -> 자동 생성 자막 찾음")
                except Exception as e:
                    print(f"   -> 모든 자막 추출 시도 실패: {str(e)}")
                    return None

        transcript_text = ' '.join([t['text'] for t in transcript_list])
        print(f"   -> 자막 추출 성공 (길이: {len(transcript_text)} 자)")
        return transcript_text
    except Exception as e:
        print(f"   -> 자막 추출 실패: {str(e)}")
        return None

def summarize_text(text):
    """OpenAI API를 사용하여 텍스트를 요약합니다."""
    print("\n3. 텍스트 요약 시작")
    try:
        if not text:
            print("   -> 텍스트가 없어 요약 불가")
            return "자막을 찾을 수 없습니다."

        if not openai.api_key:
            print("   -> OpenAI API 키가 설정되지 않음")
            return "OpenAI API 키가 설정되지 않았습니다."

        print(f"   -> OpenAI API 호출 시작 (텍스트 길이: {len(text)} 자)")
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes YouTube videos. Please provide a concise summary in Korean."},
                {"role": "user", "content": f"다음 영상의 내용을 서론, 본론, 결론으로 나누어 마크다운, 리스트 형식으로 요약해주세요.:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        print("   -> 요약 생성 완료")
        return summary
    except Exception as e:
        print(f"   -> 요약 생성 실패: {str(e)}")
        return f"요약 생성 중 오류가 발생했습니다: {str(e)}" 
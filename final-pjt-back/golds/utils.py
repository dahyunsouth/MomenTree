import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_video_id_from_url(url):
    """YouTube URL에서 비디오 ID를 추출합니다."""
    if 'youtu.be' in url:
        return url.split('/')[-1]
    elif 'youtube.com' in url:
        return url.split('v=')[1].split('&')[0]
    return url

def get_video_transcript(video_id):
    """YouTube 비디오의 자막을 가져옵니다."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        return ' '.join([t['text'] for t in transcript_list])
    except Exception as e:
        print(f"자막 추출 에러: {str(e)}")
        return None

def summarize_text(text):
    """OpenAI API를 사용하여 텍스트를 요약합니다."""
    try:
        if not text:
            return "자막을 찾을 수 없습니다."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes YouTube videos. Please provide a concise summary in Korean."},
                {"role": "user", "content": f"다음 영상의 내용을 300자 이내로 요약해주세요:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"요약 생성 에러: {str(e)}")
        return "요약 생성 중 오류가 발생했습니다." 
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_video_id_from_url, get_video_transcript, summarize_text
import os

# Create your views here.

@api_view(['POST'])
def summarize_video(request):
    """YouTube 영상을 요약하는 API 엔드포인트"""
    try:
        print("\n=== 영상 요약 시작 ===")
        print("Received request data:", request.data)
        video_url = request.data.get('video_url')
        print("Extracted video_url:", video_url)
        
        if not video_url:
            print("video_url이 없음")
            return Response({'error': 'video_url is required'}, status=400)

        print(f"Received video_url: {video_url}")
        
        video_id = get_video_id_from_url(video_url)
        print(f"Extracted video_id: {video_id}")
        
        transcript = get_video_transcript(video_id)
        if not transcript:
            print("자막을 찾을 수 없음")
            return Response({
                'error': '자막을 찾을 수 없습니다. 해당 영상에 자막이 없거나 자막을 가져올 수 없습니다.',
                'video_id': video_id
            }, status=400)
            
        print(f"자막 추출 성공 (길이: {len(transcript)}자)")
        
        if not os.getenv('OPENAI_API_KEY'):
            print("OpenAI API 키가 설정되지 않음")
            return Response({
                'error': 'OpenAI API 키가 설정되지 않았습니다.',
                'video_id': video_id
            }, status=500)
            
        summary = summarize_text(transcript)
        print("요약 생성 완료")
        return Response({
            'summary': summary,
            'video_id': video_id
        })
    except Exception as e:
        print(f"Error in summarize_video: {str(e)}")
        import traceback
        print("상세 에러:", traceback.format_exc())
        return Response({
            'error': str(e),
            'detail': traceback.format_exc(),
            'video_id': video_id if 'video_id' in locals() else None
        }, status=500)

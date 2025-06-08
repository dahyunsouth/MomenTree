from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import PriceData
from dateutil.parser import parse
import pandas as pd
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_video_id_from_url, get_video_transcript, summarize_text

def price_chart(request):
    # 차트 페이지 렌더링
    return render(request, 'golds/chart.html')

def price_api(request):
    asset_type = request.GET.get('asset', 'GOLD').upper()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    print(f"Received request - Asset: {asset_type}, Start: {start_date_str}, End: {end_date_str}")

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    except Exception as e:
        print(f"Date parsing error: {e}")
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    print(f"Parsed dates - Start: {start_date}, End: {end_date}")

    queryset = PriceData.objects.filter(asset_type=asset_type)

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    queryset = queryset.order_by('date')
    
    print(f"Found {queryset.count()} records")

    if not queryset.exists():
        return JsonResponse({
            'labels': [],
            'datasets': [{
                'label': f'{asset_type} Price',
                'data': []
            }]
        })

    data = {
        'labels': [item.date.strftime('%Y-%m-%d') for item in queryset],
        'datasets': [{
            'label': f'{asset_type} Price',
            'data': [float(item.price) for item in queryset],
            'borderColor': '#FFD700' if asset_type == 'GOLD' else '#C0C0C0'
        }]
    }

    print(f"Returning data with {len(data['labels'])} points")
    return JsonResponse(data)

@api_view(['POST'])
def summarize_video(request):
    """YouTube 영상을 요약하는 API 엔드포인트"""
    try:
        video_url = request.data.get('video_url')
        if not video_url:
            return Response({'error': 'video_url is required'}, status=400)

        video_id = get_video_id_from_url(video_url)
        transcript = get_video_transcript(video_id)
        summary = summarize_text(transcript)

        return Response({
            'summary': summary
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

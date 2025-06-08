from django.urls import path
from . import views

urlpatterns = [
    path('chart/', views.price_chart),      # 차트 페이지 렌더링
    path('api/prices/', views.price_api),     # 차트 데이터 JSON API
    path('api/summarize/', views.summarize_video, name='summarize_video'),
]

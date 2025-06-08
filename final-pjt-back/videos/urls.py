from django.urls import path
from . import views

app_name = 'videos'  # namespace 추가

urlpatterns = [
    path('summarize/', views.summarize_video, name='summarize'),  # videos/ 접두어는 상위 urls.py에서 처리
] 
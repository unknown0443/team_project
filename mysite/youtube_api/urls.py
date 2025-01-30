from django.urls import path
from . import views
from youtube_api.views import video_list, search_videos

urlpatterns = [
    path('', views.video_list, name='video_list'),  # 기본 URL에 연결
    path('search/', search_videos, name='search_videos'),  # ✅ 검색 결과 페이지 추가
]
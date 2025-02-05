from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('youtube/', include('youtube_api.urls')),  # ✅ youtube 관련 API 경로
    path('naver/', include('naver_api.urls')),  # ✅ naver 관련 API 경로
]
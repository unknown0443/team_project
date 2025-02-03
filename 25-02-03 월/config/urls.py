
from django.contrib import admin
from django.urls import path, include
from youtube_api import views  # ✅ views 직접 import

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('youtube/', include('youtube_api.urls')),  # youtube/ 경로로 접근 가능
    
    path('visualize/', views.visualize_comments, name='visualize_comments'),  # 직접 경로 추가
]

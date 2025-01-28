
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('youtube/', include('youtube_api.urls')),  # youtube/ 경로로 접근 가능
]

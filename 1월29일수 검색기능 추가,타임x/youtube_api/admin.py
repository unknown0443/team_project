from django.contrib import admin
from .models import YouTubeVideo

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'published_date')
    search_fields = ('title', 'description')
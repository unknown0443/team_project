from django.contrib import admin
from youtube_api.models import YouTubeVideo

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_id", "published_date", "captions")
    search_fields = ("title", "description")
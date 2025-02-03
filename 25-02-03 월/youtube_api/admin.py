from django.contrib import admin
from .models import YouTubeVideo, HashtagCategory, YouTubeComment

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'published_date')
    search_fields = ('title', 'description')

@admin.register(HashtagCategory)
class HashtagCategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "hashtag", "frequency")  # 컬럼 표시
    search_fields = ("category", "hashtag")  # 검색 기능 추가
    list_filter = ("category",)  # 카테고리별 필터 추가

@admin.register(YouTubeComment)
class YouTubeCommentAdmin(admin.ModelAdmin):
    list_display = ("video", "author", "published_date", "like_count")  # 컬럼 표시
    search_fields = ("comment_text", "author")  # 댓글 내용, 작성자 검색 기능 추가
    list_filter = ("published_date",)  # 날짜별 필터 추가

from django.db import models

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)  # 동영상 제목
    video_id = models.CharField(max_length=50, unique=True)  # 유튜브 동영상 ID
    description = models.TextField()  # 동영상 설명
    captions = models.TextField(null=True, blank=True)  # 자막 내용 (SRT 형식)
    published_date = models.DateTimeField(null=True, blank=True)  # 동영상 게시 날짜

    def __str__(self):
        return self.title
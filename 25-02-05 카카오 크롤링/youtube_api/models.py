from django.db import models

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)  # 동영상 제목
    video_id = models.CharField(max_length=50, unique=True)  # 유튜브 동영상 ID
    description = models.TextField()  # 동영상 설명
    captions = models.TextField(null=True, blank=True)  # 자막 내용 (SRT 형식)
    published_date = models.DateTimeField(null=True, blank=True)  # 동영상 게시 날짜

    def __str__(self):
        return self.title
    
class Place(models.Model):
    CATEGORY_CHOICES = [
        ('tourist', '관광지'),
        ('restaurant', '맛집'),
        ('cafe', '카페'),
    ]

    name = models.CharField(max_length=255)       # 장소명
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # 관광지, 맛집, 카페 구분
    address = models.CharField(max_length=300)    # 주소
    rating = models.FloatField(null=True, blank=True)  # 평점
    link = models.URLField(null=True, blank=True) # 네이버 상세 페이지 링크
    review_count = models.IntegerField(default=0)  # 🔹 기존 흐름 유지하면서 review_count 추가
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 저장 날짜

    def __str__(self):
        return self.name
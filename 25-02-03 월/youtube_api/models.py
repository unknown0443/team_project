from django.db import models

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)  # 동영상 제목
    video_id = models.CharField(max_length=50, unique=True)  # 유튜브 동영상 ID
    description = models.TextField()  # 동영상 설명
    captions = models.TextField(null=True, blank=True)  # 자막 내용 (SRT 형식)
    published_date = models.DateTimeField(null=True, blank=True)  # 동영상 게시 날짜

    def __str__(self):
        return self.title

class YouTubeComment(models.Model):
    video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE, related_name="comments")  # 동영상과 연결
    comment_text = models.TextField()  # 댓글 내용
    author = models.CharField(max_length=255, null=True, blank=True)  # 작성자 (익명 가능)
    published_date = models.DateTimeField()  # 댓글 작성 날짜 (연도별 분석용)
    like_count = models.IntegerField(default=0)  # 댓글 추천(좋아요) 수

    def __str__(self):
        return f"Comment on {self.video.title} by {self.author}"


class KeywordTrend(models.Model):
    keyword = models.CharField(max_length=100)  # 키워드
    frequency = models.IntegerField()  # 등장 빈도수
    year = models.IntegerField()  # 연도

    def __str__(self):
        return f"{self.year} - {self.keyword} ({self.frequency})"
    

class HashtagCategory(models.Model):
    category = models.CharField(max_length=50)  # 예: 맛집, 숙소, 장소
    hashtag = models.CharField(max_length=100)  # 해시태그 (예: #부산맛집)
    frequency = models.IntegerField()  # 등장 빈도

    def __str__(self):
        return f"{self.category} - {self.hashtag} ({self.frequency}회)"
    
class Comment(models.Model):
    video_id = models.CharField(max_length=100)  # 유튜브 영상 ID
    text = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    def __str__(self):
        return f"{self.video_id}: {self.text[:30]}"  # 댓글 앞부분만 표시
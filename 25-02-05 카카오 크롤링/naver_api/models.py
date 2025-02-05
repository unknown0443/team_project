from django.db import models

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('tourist', '관광지'),
        ('restaurant', '맛집'),
        ('cafe', '카페'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    address = models.CharField(max_length=300)
    rating = models.FloatField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'naver_api'  # ✅ 앱명을 명시
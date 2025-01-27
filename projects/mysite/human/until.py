from googleapiclient.discovery import build
from .models import YouTubeVideo
from human.utils import fetch_videos_with_subtitles

# YouTube API 키 설정
API_KEY = 'AIzaSyDITzhsLU6Q2bXLn3cS-04UXGndyLAF2jA'

def fetch_videos_with_subtitles(query, max_results=50):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # YouTube에서 동영상 검색
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        videoCaption='closedCaption'  # 자막이 있는 동영상만 필터링
    )
    response = request.execute()

    for item in response.get('items', []):
        video_data = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'description': item['snippet'].get('description', ''),
            'published_at': item['snippet']['publishedAt'],
            'has_subtitles': True,
        }

        # 데이터베이스에 저장
        YouTubeVideo.objects.update_or_create(
            video_id=video_data['video_id'],
            defaults=video_data
        )

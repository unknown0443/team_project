import os
import django
import json
import re
from googleapiclient.discovery import build
from pytube import YouTube
from youtube_api.models import YouTubeVideo

# ✅ Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# ✅ JSON 파일에서 API 키 불러오기 (네이버 API 제외)
config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)
    YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]

# ✅ YouTube API 설정
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# ✅ YouTube 영상 검색 기능 (기존 코드 유지)
def search_videos_with_captions(query, max_results=50, page_token=None):
    try:
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            videoCaption="closedCaption",
            maxResults=max_results,
            pageToken=page_token  
        ).execute()

        videos = []
        next_page_token = search_response.get("nextPageToken")

        for item in search_response.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "description": item["snippet"]["description"],
                "published_date": item["snippet"]["publishedAt"],
            })

        return videos, next_page_token  

    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return [], None  
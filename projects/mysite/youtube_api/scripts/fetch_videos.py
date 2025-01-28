import os
import sys
import django

# 현재 스크립트의 경로를 기준으로 Django 프로젝트 루트 경로를 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# YouTube API 유틸리티 함수 임포트
from youtube_api.utils import search_videos_with_captions, save_video_and_captions

def fetch_and_save_videos():
    """
    "부산 여행" 키워드로 YouTube 동영상을 검색하고, PostgreSQL에 저장합니다.
    """
    query = "부산 여행"  # 검색 키워드
    print(f"Searching for videos with query: {query}")

    # YouTube API를 사용해 동영상 검색
    videos = search_videos_with_captions(query, max_results=10)

    # 검색 결과를 저장
    for video_data in videos:
        save_video_and_captions(video_data)
    print("Video fetching and saving completed.")

# 스크립트 직접 실행 시 동작
if __name__ == "__main__":
    fetch_and_save_videos()
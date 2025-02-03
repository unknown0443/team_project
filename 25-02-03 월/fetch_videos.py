import os
import sys
import django
import json
from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from pytube import YouTube
from youtube_api.models import YouTubeVideo, Comment  # ✅ Comment 모델 추가

# ✅ Django 프로젝트 루트 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 경로
project_root = os.path.dirname(current_dir)  # 프로젝트 루트 (mysite/)
sys.path.append(project_root)

# ✅ Django 환경 설정 강제 로드 (설정 파일 위치 확인 필요)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # 프로젝트 설정에 맞게 수정

# ✅ Django 환경을 설정한 후에 setup 실행
django.setup()  # ✅ Django 환경 초기화 (여기서 먼저 실행해야 함)

# ✅ Django 설정이 적용된 후 모델 import (순서 중요)
from youtube_api.models import YouTubeVideo, Comment
from youtube_api.utils import search_videos_with_captions
from youtube_transcript_api import YouTubeTranscriptApi

def download_captions(video_id):
    """
    YouTube 동영상에서 자막을 가져옵니다. (자동 생성 포함)
    """
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(video_url)

        available_captions = yt.captions
        print(f"🔍 Available captions for {video_id}: {list(available_captions.keys())}")

        if available_captions:
            preferred_languages = ['ko']
            for lang in preferred_languages:
                if lang in available_captions:
                    caption = available_captions[lang]
                    srt_captions = caption.generate_srt_captions()
                    print(f"✅ Downloaded captions for {video_id} using `pytube`.")
                    return srt_captions
        
        # ✅ `pytube`에서 자막이 없으면 `youtube_transcript_api` 사용
        print(f"⚠️ No captions found via `pytube`. Trying `youtube_transcript_api`...")
        
        transcript = None
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        except:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            except:
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                except Exception as e:
                    print(f"❌ No available transcripts: {e}")
                    return None

        if transcript:
            srt_captions = "\n".join([f"{entry['start']} --> {entry['start'] + entry['duration']}\n{entry['text']}" for entry in transcript])
            print(f"✅ Downloaded captions for {video_id} using `youtube_transcript_api`.")
            return srt_captions

    except Exception as e:
        print(f"⚠️ Error downloading captions for {video_id}: {e}")
        return None  # 자막이 없으면 None 반환

def save_video_and_captions(video_data):
    """
    YouTube 동영상 정보를 DB에 저장하고 자막을 다운로드 후 저장.
    """
    try:
        video, created = YouTubeVideo.objects.get_or_create(
            video_id=video_data['video_id'],
            defaults={
                'title': video_data['title'],
                'description': video_data['description'],
                'captions': None,  # 기본값 None
                'published_date': video_data['published_date'],
            }
        )

        # ✅ 자막 다운로드
        captions = download_captions(video.video_id)
        if captions:
            video.captions = captions  # DB에 자막 저장
            video.save()
            print(f"✅ Saved captions for {video.video_id}")
        else:
            print(f"❌ No captions available for {video.video_id}")

    except Exception as e:
        print(f"⚠️ Error saving video and captions: {e}")

def fetch_and_save_videos():
    """
    기존 DB에 저장된 영상들의 자막을 업데이트.
    """
    videos = YouTubeVideo.objects.all()

    for video in videos:
        print(f"🎬 Checking captions for {video.title} ({video.video_id})")

        # 자막 다운로드 테스트
        captions = download_captions(video.video_id)

        if captions:
            video.captions = captions
            video.save()
            print(f"✅ Captions updated for {video.video_id}\n")
        else:
            print(f"❌ No captions available for {video.video_id}\n")

def fetch_and_save_new_videos(query="부산 여행", max_results=300):
    """
    YouTube API에서 새로운 영상을 검색하고 DB에 추가 후 자막을 다운로드.
    자막이 있는 영상만 필터링하여 저장. 페이지 토큰을 활용해 50개 이상 가져옴.
    """
    print(f"🔍 Searching YouTube for '{query}' with captions only...")

    video_results = []
    next_page_token = None

    while len(video_results) < max_results:
        remaining = max_results - len(video_results)
        new_videos, next_page_token = search_videos_with_captions(query, max_results=min(50, remaining), page_token=next_page_token)

        if not new_videos:
            break  # 더 이상 가져올 데이터가 없으면 중단

        video_results.extend(new_videos)

        if not next_page_token:
            break  # 다음 페이지가 없으면 중단

    if not video_results:
        print(f"❌ No videos found for '{query}'.")
        return

    for video_data in video_results:
        print(f"🎬 Found video: {video_data['title']} ({video_data['video_id']})")

        # ✅ DB에 없는 경우에만 새로 저장
        video, created = YouTubeVideo.objects.get_or_create(
            video_id=video_data["video_id"],
            defaults={
                "title": video_data["title"],
                "description": video_data["description"],
                "captions": None,  # 기본값 None
                "published_date": video_data["published_date"],
            }
        )

        if created:
            print(f"✅ New video saved: {video.video_id}")
        else:
            print(f"⚠️ Video already exists: {video.video_id}")

        # ✅ 자막 다운로드
        captions = download_captions(video.video_id)
        if captions:
            video.captions = captions  # DB에 자막 저장
            video.save()
            print(f"✅ Captions saved for {video.video_id}")
        else:
            print(f"❌ No captions available for {video.video_id} (Skipping)")

    print(f"🎉 Fetching complete! Total new videos added: {len(video_results)}")

# ✅ 실행
if __name__ == "__main__":
    search_query = "부산 여행"  # 🔍 검색어 설정
    fetch_and_save_new_videos(search_query, max_results=300)  # ✅ 새로운 영상 300개 추가
    fetch_and_save_videos()  # ✅ 기존 영상 자막 업데이트

# ✅ YouTube API 설정 (API 키 입력 필요)
with open("config.json", "r") as config_file:
    config = json.load(config_file)  # JSON 파일을 파싱
    API_KEY = config.get("YOUTUBE_API_KEY", None)

if API_KEY is None:
    raise ValueError("❌ 유효한 YouTube API 키가 없습니다. config.json 파일을 확인하세요.")

def fetch_comments(video_id, max_results=50):
    """
    YouTube API를 사용하여 특정 영상의 댓글을 가져옵니다.
    """
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results
        )
        response = request.execute()

        comments = []
        for item in response.get("items", []):
            comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            comments.append({"user": author, "comment": comment_text})

        return comments
    except Exception as e:
        print(f"❌ 댓글을 가져오는 중 오류 발생: {e}")
        return []    

def fetch_and_save_comments():
    """
    DB에 저장된 모든 영상의 댓글을 200개씩 가져와 저장
    """
    videos = YouTubeVideo.objects.all()

    for video in videos:
        print(f"📥 Fetching up to 200 comments for: {video.title} ({video.video_id})")

        comments = fetch_comments(video.video_id, max_results=100, total_comments=200)
        if not comments:
            print(f"⚠️ No comments found for {video.video_id}")
            continue

        for comment_data in comments:
            Comment.objects.get_or_create(
                video=video,
                user=comment_data["user"],
                comment=comment_data["comment"]
            )

        print(f"✅ {len(comments)} comments saved for {video.video_id}")

# ✅ 실행
if __name__ == "__main__":
    fetch_and_save_comments()
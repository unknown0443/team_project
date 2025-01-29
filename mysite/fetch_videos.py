import os
import django
import sys
from pytube import YouTube


# ✅ Django 프로젝트 루트를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 경로
project_root = os.path.dirname(current_dir)  # 프로젝트 루트 (mysite/)
sys.path.append(project_root)

# 현재 스크립트의 디렉토리를 Django 프로젝트 루트로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Django 환경 설정 (코드 맨 위에서 실행)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()  # Django 앱 초기화

from youtube_api.models import YouTubeVideo
from youtube_api.utils import search_videos_with_captions, download_captions
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
            preferred_languages = ['ko', 'en', 'a.en']
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
    YouTube 동영상 정보를 PostgreSQL에 저장하고 자막을 다운로드 후 저장.
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

        # ✅ 자막 다운로드 (video_id 사용)
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
    데이터베이스에서 동영상 목록을 가져오고 자막을 다운로드 후 저장.
    """
    videos = YouTubeVideo.objects.all()

    for video in videos:
        print(f"🎬 Checking captions for {video.title} ({video.video_id})")

        # 저장된 video_id를 기반으로 자막 다운로드 테스트
        captions = download_captions(video.video_id)

        if captions:
            video.captions = captions
            video.save()
            print(f"✅ Captions saved for {video.video_id}\n")
        else:
            print(f"❌ No captions available for {video.video_id}\n")


# ✅ 실행
if __name__ == "__main__":
    fetch_and_save_videos()
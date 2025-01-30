from googleapiclient.discovery import build
from pytube import YouTube
from .models import YouTubeVideo
import re


# YouTube API 설정
API_KEY = 'AIzaSyDITzhsLU6Q2bXLn3cS-04UXGndyLAF2jA'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos_with_captions(query, max_results=5):
    """
    YouTube API로 자막이 포함된 동영상을 검색합니다.
    """
    try:
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            videoCaption='closedCaption',
            maxResults=max_results
        ).execute()

        videos = []
        for item in search_response['items']:
            video_data = {
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'description': item['snippet']['description'],
                'published_date': item['snippet']['publishedAt'],
            }
            videos.append(video_data)
        return videos
    except Exception as e:
        print(f"Error: {e}")
        return []

def save_video_and_captions(video_data):
    """
    동영상 정보와 자막을 PostgreSQL에 저장합니다.
    """
    try:
        video_url = f"https://www.youtube.com/watch?v={video_data['video_id']}"
        yt = YouTube(video_url)

        # 자막 다운로드
        captions = None
        if yt.captions:
            caption = yt.captions.get_by_language_code('en')  # 영어 자막
            if caption:
                captions = caption.generate_srt_captions()

        # 데이터베이스 저장
        video, created = YouTubeVideo.objects.get_or_create(
            video_id=video_data['video_id'],
            defaults={
                'title': video_data['title'],
                'description': video_data['description'],
                'captions': captions,
                'published_date': video_data['published_date'],
            }
        )
        if created:
            print(f"Saved video: {video.title}")
        else:
            print(f"Video already exists: {video.title}")
    except Exception as e:
        print(f"Error saving video and captions: {e}")

def parse_srt_captions(srt_data):
    """
    SRT 형식의 자막 데이터를 분석하여 타임스탬프와 문장을 반환합니다.
    """
    if not srt_data:
        return []

    # SRT 패턴 정의
    srt_pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+)"
    matches = re.findall(srt_pattern, srt_data, re.DOTALL)

    parsed_captions = []
    for match in matches:
        start_time = match[1]  # 자막 시작 시간
        end_time = match[2]    # 자막 끝 시간
        text = match[3].replace("\n", " ")  # 자막 내용 (줄바꿈 제거)
        parsed_captions.append({
            "start_time": start_time,
            "end_time": end_time,
            "text": text
        })

    return parsed_captions        

def download_captions(video_id):
    """
    YouTube 동영상에서 자막을 가져옵니다.
    """
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(video_url)

        # 가용한 자막 목록 확인
        available_captions = yt.captions
        print(f"Available captions: {available_captions}")

        if not yt.captions:
            print(f"❌ No captions available for video ID: {video_id}")
            return None

        # 자막을 우선적으로 가져올 언어 리스트 (영어, 한국어, 자동 생성 포함)
        preferred_languages = ['ko', 'en', 'a.en']  # 한국어, 영어, 자동 생성 영어
        caption = None

        for lang in preferred_languages:
            if lang in yt.captions:
                caption = yt.captions[lang]
                break

        if caption:
            srt_captions = caption.generate_srt_captions()
            print(f"✅ Downloaded captions for {video_id}: {srt_captions[:100]}...")
            return srt_captions
        else:
            print(f"❌ No preferred captions found for video ID: {video_id}")

    except Exception as e:
        print(f"⚠️ Error downloading captions: {e}")

    return None  # 자막이 없으면 None 반환
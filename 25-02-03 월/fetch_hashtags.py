import re
import django
import os
import sys
from collections import defaultdict, Counter
from googleapiclient.discovery import build
import json

# Django ORM 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from youtube_api.models import HashtagCategory

# 유튜브 API 설정 (API 키 불러오기)
config_path = os.path.join(current_dir, "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)  # JSON 파일을 파싱
    API_KEY = config["YOUTUBE_API_KEY"]
youtube = build("youtube", "v3", developerKey=API_KEY)

# 🔹 초기 장소 리스트 (기존보다 확장)
PLACE_LIST = [
    "해운대", "광안리", "태종대", "감천문화마을", "오륙도", "송정해수욕장", "BIFF광장",
    "자갈치시장", "부산타워", "해동용궁사", "동백섬", "송도해수욕장", "부산시립미술관",
    "국제시장", "송도케이블카", "부산롯데월드", "용두산공원", "부산항대교", "누리마루APEC하우스"
]

# 정규 표현식으로 해시태그 찾기
HASHTAG_PATTERN = re.compile(r"#(\w+)")

def fetch_videos(query, max_results=15):
    """ 특정 장소를 검색하여 유튜브 영상 가져오기 """
    video_ids = []
    next_page_token = None

    while len(video_ids) < max_results:
        request = youtube.search().list(
            q=query,
            part="id",
            type="video",
            maxResults=min(50, max_results - len(video_ids)),
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get("items", []):
            video_ids.append(item["id"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # 더 이상 가져올 데이터가 없으면 중단

    return video_ids

def get_video_details(video_ids):
    """ 유튜브 영상 ID 리스트를 입력받아 상세 정보를 가져오는 함수 """
    if not video_ids:  
        print("⚠️ 오류: video_ids 리스트가 비어 있음!")
        return []  # 비어 있을 경우 빈 리스트 반환

    video_data = []
    
    # 유튜브 API 요청은 한 번에 최대 50개까지 가능
    for i in range(0, len(video_ids), 15):
        request = youtube.videos().list(
            part="snippet",
            id=",".join(video_ids[i:i+15])  # 🔹 최대 50개씩 요청
        )
        response = request.execute()

        for item in response.get("items", []):  # 🔹 get("items")로 에러 방지
            video_data.append({
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "tags": item["snippet"].get("tags", [])  # 🔹 영상 태그까지 가져오기
            })

    return video_data

def fetch_additional_places():
    """ '부산 가볼만한 곳' 검색하여 새로운 장소 자동 추가 """
    print("🔍 '부산 가볼만한 곳' 검색 중...")
    video_ids = fetch_videos(query="부산 가볼만한 곳", max_results=50)
    videos = get_video_details(video_ids)

    new_places = set()
    for video in videos:
        hashtags = HASHTAG_PATTERN.findall(video["description"])  # 설명에서 해시태그 추출
        new_places.update(hashtags)  # 새로운 장소 후보 저장

    # 기존 장소 리스트에 추가
    additional_places = [place for place in new_places if place not in PLACE_LIST]
    PLACE_LIST.extend(additional_places)

    print(f"✅ 새로운 장소 {len(additional_places)}개 추가 완료!")
    print(f"📌 최종 장소 리스트: {PLACE_LIST}")

def categorize_places():
    """ 장소 리스트 기반으로 검색하여 해시태그 데이터 확보 """
    fetch_additional_places()  # 새로운 장소 리스트 업데이트
    all_video_ids = set()
    all_videos = []

    for place in PLACE_LIST:
        print(f"🔍 '{place}' 검색 중...")
        video_ids = fetch_videos(query=place, max_results=50)
        all_video_ids.update(video_ids)
        print(f"✅ '{place}'에서 {len(video_ids)}개의 영상 가져옴.")

    print(f"🎬 총 {len(all_video_ids)}개의 유튜브 영상 데이터 수집 완료!")
    return get_video_details(list(all_video_ids))

# 실행
if __name__ == "__main__":
    categorize_places()

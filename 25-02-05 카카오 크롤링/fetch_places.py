import json
import requests
import os
import sys
import django

# ✅ 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from naver_api.models import Place  # Django 모델 불러오기
from naver_api.utils import process_places  # 데이터 가공 함수

# ✅ 네이버 API 키 불러오기
config_path = os.path.join(os.path.dirname(__file__), "config.json")  # 경로 수정
with open(config_path, "r") as config_file:
    config = json.load(config_file)
    NAVER_CLIENT_ID = config["NAVER_CLIENT_ID"]
    NAVER_CLIENT_SECRET = config["NAVER_CLIENT_SECRET"]

# ✅ 네이버 API를 사용하여 장소 정보 가져오기
def fetch_places(query, display=50):
    """네이버 API에서 장소 데이터를 가져오는 함수"""
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display, "start": 1, "sort": "comment"}  # ✅ 리뷰 많은 순 정렬

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"❌ 네이버 API 호출 실패: {response.status_code}")
        return []

# ✅ 가져온 데이터를 DB에 저장하는 함수
def save_places():
    """네이버 API에서 데이터를 가져와 DB에 저장하는 함수"""
    queries = {
        "tourist": "부산 관광지",
        "restaurant": "부산 맛집",
        "cafe": "부산 카페"
    }

    places_to_add = []
    for category, query in queries.items():
        data = fetch_places(query, display=50)  # ✅ API에서 최대 50개 가져오기
        processed_places = process_places(data, category) if data else []

        for place in processed_places:
            places_to_add.append(Place(
                name=place.get("name", "Unknown"),  # 기본값 설정
                category=place.get("category", category),  # 기본값 설정
                address=place.get("address", "주소 정보 없음"),  # 기본값 설정
                rating=place.get("rating", 0.0),  # 기본값 설정
                review_count=place.get("review_count", 0),  # 기본값 설정
                link=place.get("link", ""),  # 기본값 설정
            ))

    if places_to_add:
        Place.objects.bulk_create(places_to_add, ignore_conflicts=True)  # ✅ 중복 데이터 방지
        print(f"✅ {len(places_to_add)}개 장소 데이터 추가 완료!")
    else:
        print("❌ 새로운 데이터 없음.")

# ✅ 스크립트를 실행하면 자동으로 실행되도록 설정
if __name__ == "__main__":
    print("✅ 네이버 API에서 데이터를 가져오는 중...")
    save_places()
    print("✅ 네이버 데이터 가져오기 완료!")

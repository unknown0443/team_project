import random

# ✅ 네이버 API에서 가져온 데이터를 정제하는 함수
def process_places(data, category):
    """ 네이버 API에서 가져온 데이터를 정제하는 함수 """
    places = []
    for place in data:
        places.append({
            "name": place['title'].replace("<b>", "").replace("</b>", ""),
            "category": category,
            "address": place.get('roadAddress', "주소 없음"),
            "rating": round(random.uniform(3.5, 5.0), 1),  # ✅ 임시 평점 (추후 개선)
            "review_count": random.randint(100, 500),  # ✅ 임시 리뷰 수 (추후 개선)
            "link": place.get('link', "https://naver.com")
        })
    return places

def format_timestamp(seconds):
    """ 초 단위 시간을 hh:mm:ss 형식으로 변환 """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

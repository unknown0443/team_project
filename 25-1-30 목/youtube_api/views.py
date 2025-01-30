from django.shortcuts import render
from youtube_api.models import YouTubeVideo
from django.db.models import Q
import re
from youtube_api.utils import format_timestamp  

def video_list(request):
    """
    저장된 동영상 리스트를 불러와 HTML로 렌더링.
    """
    videos = YouTubeVideo.objects.filter(captions__isnull=False)  # ✅ 자막이 있는 것만 필터링

    return render(request, "video_list.html", {"videos": videos})  # ✅ 변경된 경로 반영

def search_videos(request):
    """
    검색 기능 (자막에서 검색어 포함된 부분을 찾아서 표시)
    """
    query = request.GET.get('q', '')  # 검색어 가져오기
    videos = YouTubeVideo.objects.exclude(captions__isnull=True)  # 자막이 있는 동영상만 검색

    search_results = []  # 검색 결과 저장 리스트

    if query:
        for video in videos:
            matched_captions = []
            captions = video.captions.split("\n")  # 자막을 줄 단위로 분할

            for i in range(len(captions)):
                line = captions[i]

                if query in line:  # 검색어 포함된 자막 찾기
                    if i > 0 and "-->" in captions[i - 1]:  
                        timestamp = captions[i - 1].split("-->")[0].strip()  # 시작 시간만 추출
                    else:
                        timestamp = "0"  # 기본값 (초 단위)

                    print(f"🎯 [views.py] 추출된 timestamp: {timestamp}")  # ✅ 디버깅: 실제 값 확인

                    try:
                        # ✅ timestamp가 초 단위 (float) 값이면 변환
                        seconds = float(timestamp)
                        formatted_time = format_timestamp(int(seconds))  # 🔹 정수로 변환 후 hh:mm:ss 적용
                        print(f"✅ [views.py] 변환된 시간: {formatted_time} ({seconds}초)")  # ✅ 변환된 값 확인
                    except ValueError:
                        print(f"❌ [views.py] timestamp 변환 실패: {timestamp}")  # ✅ 변환 실패 디버깅
                        seconds = 0
                        formatted_time = "00:00:00"

                    matched_captions.append({
                        "time": formatted_time,  # ✅ 변환된 시간 적용 (00:01:25 같은 형식)
                        "seconds": int(seconds),  # 초 단위 (정수형)
                        "text": line.strip()  # 검색된 자막
                    })

            if matched_captions:
                search_results.append({
                    "video_id": video.video_id,
                    "title": video.title,
                    "matches": matched_captions
                })

    return render(request, "search_results.html", {"query": query, "search_results": search_results})
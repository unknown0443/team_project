from django.shortcuts import render
from youtube_api.models import YouTubeVideo
from django.core.paginator import Paginator
from naver_api.utils import format_timestamp  

def video_list(request):
    """
    저장된 모든 동영상 리스트를 불러와 HTML로 렌더링 (타임스탬프 변환 추가).
    """
    videos = YouTubeVideo.objects.filter(captions__isnull=False)  # ✅ 자막 있는 동영상만 가져오기
    video_data = []

    for video in videos:
        matched_captions = []
        captions = video.captions.split("\n")  # 자막을 줄 단위로 분할

        for i in range(len(captions)):
            line = captions[i]

            if "-->" in line:  # ✅ 타임스탬프 줄이면 처리
                timestamp = line.split("-->")[0].strip()  # 시작 시간 추출
                try:
                    seconds = float(timestamp)
                    formatted_time = format_timestamp(int(seconds))  # 🔹 hh:mm:ss 변환
                except ValueError:
                    seconds = 0
                    formatted_time = "00:00:00"
                continue  

            if line.strip():
                matched_captions.append({
                    "time": formatted_time,
                    "seconds": int(seconds),
                    "text": line.strip()
                })

        video_data.append({
            "video_id": video.video_id,
            "title": video.title,
            "captions": matched_captions
        })

    paginator = Paginator(video_data, 5)  
    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)  

    return render(request, "video_list.html", {"page_obj": page_obj})

def search_videos(request):
    """
    검색 기능 (자막에서 검색어 포함된 부분을 찾아서 표시)
    """
    query = request.GET.get('q', '')  
    videos = YouTubeVideo.objects.exclude(captions__isnull=True)  

    search_results = []  

    if query:
        for video in videos:
            matched_captions = []
            captions = video.captions.split("\n")

            for i in range(len(captions)):
                line = captions[i]

                if query in line:
                    if i > 0 and "-->" in captions[i - 1]:  
                        timestamp = captions[i - 1].split("-->")[0].strip()  
                    else:
                        timestamp = "0"  

                    try:
                        seconds = float(timestamp)
                        formatted_time = format_timestamp(int(seconds))  
                    except ValueError:
                        seconds = 0
                        formatted_time = "00:00:00"

                    matched_captions.append({
                        "time": formatted_time,
                        "seconds": int(seconds),
                        "text": line.strip()
                    })

            if matched_captions:
                search_results.append({
                    "video_id": video.video_id,
                    "title": video.title,
                    "matches": matched_captions
                })

    paginator = Paginator(search_results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "search_results.html", {
        "query": query,
        "page_obj": page_obj
    })

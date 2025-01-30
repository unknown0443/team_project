from django.shortcuts import render
from youtube_api.models import YouTubeVideo
from django.db.models import Q

def video_list(request):
    """ 검색 기능 확장: 검색어가 포함된 자막이 있는 동영상만 표시 """
    query = request.GET.get("q", "").strip()  # 🔹 GET 요청에서 검색어 가져오기
    
    videos = YouTubeVideo.objects.filter(captions__isnull=False)  # 기본적으로 자막이 있는 영상만
    
    filtered_videos = []
    search_results = {}  # 검색된 자막을 저장할 딕셔너리

    if query:
        for video in videos:
            matched_captions = [
                line for line in video.captions.splitlines() if query in line  # 검색어가 포함된 자막만 필터링
            ]
            if matched_captions:
                filtered_videos.append(video)  # 검색된 자막이 포함된 영상만 리스트에 추가
                search_results[video.video_id] = matched_captions  # 해당 영상의 검색된 자막 저장
    else:
        search_results = {video.video_id: video.captions.splitlines() for video in videos}  # 모든 자막 표시

    return render(request, "video_list.html", {
        "videos": filtered_videos if query else videos,
        "search_results": search_results,
        "query": query
    })

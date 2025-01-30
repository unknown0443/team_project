from django.shortcuts import render
from .models import YouTubeVideo
from .utils import parse_srt_captions


def video_list(request):
    """
    저장된 동영상 정보를 웹페이지에 표시합니다.
    """
    videos_with_captions = []

    # 동영상 데이터와 파싱된 자막 준비
    videos = YouTubeVideo.objects.all()
    for video in videos:
        parsed_captions = parse_srt_captions(video.captions)  # 자막 파싱
        videos_with_captions.append({
            "video": video,
            "captions": parsed_captions
        })

    return render(request, 'video_list.html', {'videos_with_captions': videos_with_captions})
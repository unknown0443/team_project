from django.shortcuts import render
from youtube_api.models import YouTubeVideo
from django.db.models import Q
import re
from youtube_api.utils import format_timestamp 
from django.core.paginator import Paginator 
from .models import Comment
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import io
import base64



def video_list(request):
    """
    저장된 모든 동영상 리스트를 불러와 HTML로 렌더링 (타임스탬프 변환 추가).
    """
    videos = YouTubeVideo.objects.filter(captions__isnull=False)  # ✅ 자막 있는 동영상만 가져오기
    
    video_data = []  # ✅ 가공된 데이터 저장할 리스트

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
                continue  # ✅ 실제 텍스트가 있는 줄로 이동

            if line.strip():  # ✅ 빈 줄이 아닌 경우만 저장
                matched_captions.append({
                    "time": formatted_time,  # ✅ 변환된 hh:mm:ss 포맷
                    "seconds": int(seconds),  # 초 단위
                    "text": line.strip()  # ✅ 실제 자막 텍스트
                })

        video_data.append({
            "video_id": video.video_id,
            "title": video.title,
            "captions": matched_captions  # ✅ 변환된 자막 포함
        })

    # ✅ 페이지네이션 적용
    paginator = Paginator(video_data, 5)  
    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)  

    return render(request, "video_list.html", {"page_obj": page_obj})


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

    
     # ✅ 페이지네이션 추가 (5개씩)
    paginator = Paginator(search_results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "search_results.html", {
        "query": query,
        "page_obj": page_obj  # ✅ 템플릿에서 사용 가능
    })

def dashboard(request):
    """
    간단한 대시보드 데이터 표시
    """
    data = {
        "top_videos": [
            {"title": "부산 BEST 2", "views": 12345, "likes": 678},
            {"title": "부산 여행 BEST 23", "views": 9876, "likes": 543},
        ]
    }
    return render(request, 'dashboard.html', data)

# ✅ Word Cloud 생성 함수
def generate_wordcloud(comments):
    text = " ".join(comments)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# ✅ Count Plot 생성 함수
def generate_countplot(comments):
    df = pd.DataFrame(comments, columns=["comment"])
    df["word_count"] = df["comment"].apply(lambda x: len(x.split()))

    plt.figure(figsize=(6, 4))
    sns.countplot(x=df["word_count"])
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")

    img = io.BytesIO()
    plt.savefig(img, format='PNG', bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# ✅ 댓글 시각화 페이지
def visualize_comments(request):
    comments = Comment.objects.values_list("comment", flat=True)
    
    if comments:
        wordcloud_img = generate_wordcloud(comments)
        countplot_img = generate_countplot(comments)
    else:
        wordcloud_img, countplot_img = None, None

    return render(request, "youtube_api/visualization.html", {
        "wordcloud_img": wordcloud_img,
        "countplot_img": countplot_img,
    })

def visualize_comments(request):
    """
    DB에 저장된 댓글을 가져와 Word Cloud 및 Count Plot을 생성
    """
    comments = Comment.objects.values_list("comment", flat=True)

    if comments:
        wordcloud_img = generate_wordcloud(comments)
        countplot_img = generate_countplot(comments)
    else:
        wordcloud_img, countplot_img = None, None

    return render(request, "youtube_api/visualization.html", {
        "wordcloud_img": wordcloud_img,
        "countplot_img": countplot_img,
    })

from django.shortcuts import render
from .models import Place

def dashboard(request):
    """ 관광지, 맛집, 카페 데이터를 가져와서 대시보드 페이지에 전달 및 검색 기능 추가 """
    query = request.GET.get("q", "")

    if query:
        tourist_places = Place.objects.filter(category='tourist', name__icontains=query)
        restaurant_places = Place.objects.filter(category='restaurant', name__icontains=query)
        cafe_places = Place.objects.filter(category='cafe', name__icontains=query)
    else:
        tourist_places = Place.objects.filter(category='tourist').order_by("-created_at")[:10]
        restaurant_places = Place.objects.filter(category='restaurant').order_by("-created_at")[:10]
        cafe_places = Place.objects.filter(category='cafe').order_by("-created_at")[:10]

    return render(request, "dashboard.html", {
        "tourist_places": tourist_places,
        "restaurant_places": restaurant_places,
        "cafe_places": cafe_places,
        "query": query
    })
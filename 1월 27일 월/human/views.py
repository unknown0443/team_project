from django.http import HttpResponse


def index(request):
    return HttpResponse("휴먼원정대에 오신것을 환영합니다")
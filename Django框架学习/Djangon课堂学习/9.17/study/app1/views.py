import datetime

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. 我已经在app的index中了.")


def get_time(request):
    """返回当前的时间"""
    # 老师的要求是年月日
    return HttpResponse(f"{datetime.date.today()}")
    # 动态刷新时间
    # return render(request, "app1/get_time.html")


def test(request, str1, int1, uuid1, path1):
    """内置的转换器"""
    # 现在你可以使用这些参数了
    response_text = f"字符串: {str1}<br>"
    response_text += f"整数: {int1}<br>"
    response_text += f"UUID: {uuid1}<br>"
    response_text += f"路径: {path1}<br>"
    return HttpResponse(response_text)


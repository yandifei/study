from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def show_mobile(request, phone_num):
    return HttpResponse(f'手机号为：{phone_num}')


def show_year(request, year):
    return HttpResponse(f'年份：{year}')


def show_year_month(request, year, month):
    return HttpResponse(f'{year}年{month}月')


def number(request, show_num):
    return HttpResponse(f'数字:{show_num}')

def index(request):
    return HttpResponse("Hello World")



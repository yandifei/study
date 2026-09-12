from django.http import HttpResponse
from django.shortcuts import reverse


def login(request):
    return HttpResponse('你好！')


def report(request):
    return HttpResponse('显示报告信息...')


def show_num(request, num):
    return HttpResponse(f'数字：{num}')


def blog(request, blog_id):
    return HttpResponse(f'参数blog_id值为：{blog_id}')


def book(request, name):
    return HttpResponse(f'book-{name}')


def column(request, name):
    return HttpResponse(f'column-{name}')


def index(request):
    return HttpResponse(f"users应用的反向解析的url为：{reverse('users:index')}")

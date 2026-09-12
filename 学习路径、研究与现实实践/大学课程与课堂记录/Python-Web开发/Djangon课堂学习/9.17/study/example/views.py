from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def show_mobile(request, phone_num):
    return HttpResponse(f'手机号为：{phone_num}')

def show_year(request,year):
    return HttpResponse(f'{year}年')

def show_year_month(request,year,month):
    return HttpResponse(f'{year}年{month}月')

def show_mail(request, mail_num):
    """邮箱匹配和显示"""
    return HttpResponse(f'邮箱为：{mail_num}')



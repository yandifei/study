from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import reverse


def get_url(request):
    return HttpResponse(f"反向解析的url为：{reverse('url')}")


def index(request):
    return HttpResponse(f"goods应用的反向解析的url为：{reverse('goods:index')}")


from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("你好世界。您位于民意调查索引处。")
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import reverse


# Create your views here.
# def url_path(request):
#     return HttpResponse(f"当前url:{(reverse('app01:url_path'))}")

def url_path(request):
    return HttpResponse(f"当前url:{(reverse('app01:url_path', current_app=request.resolver_match.namespace))}")

#chapter3\useAppNamespace\views.py
from django.http import HttpResponse
from django.urls import reverse
def index(request,data=0):
    s='应用默认页面URL，reverse("Default")=%s' % (reverse("myAppUrlNamespace:Default"))
    s+='<br/>获取数据页面URL，reverse("nData",args=[%s])=%s' \
                         %  (data,reverse("myAppUrlNamespace:nData",args=[data]))
    return HttpResponse(s)

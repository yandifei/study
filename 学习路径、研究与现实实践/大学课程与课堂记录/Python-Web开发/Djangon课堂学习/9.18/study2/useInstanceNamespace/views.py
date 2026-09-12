#chapter3\useInstanceNamespace\views.py
from django.http import HttpResponse
from django.urls import reverse
def index(request,data=0):
    s='应用默认页面URL，reverse("nameIndex:Default")=%s' % (reverse("nameIndex:Default"))
    s+='<br/>获取数据页面URL，reverse("nameIndex:nData",args=[%s])=%s' \
        % (data,reverse("nameIndex:nData",args=[data]))
    return HttpResponse(s)

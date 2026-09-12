#chapter3\chapter3\views.py
from django.http import HttpResponse

def CharInUrl(request):
    return HttpResponse("视图函数CharInUrl：只包含了大小写字母的URL")

def NumberInUrl(request):
    return HttpResponse("视图函数NumberInUrl：只包含了数字的URL")

def getData(request,urlData):
    return HttpResponse("从URL获取的数据："+urlData)

def getData2(request,Data1,Data2):
    return HttpResponse("从URL获取的数据：%s，%s"%(Data1,Data2))

from html import escape	#用于转换数据类型名称中的小于和大于符号，以便在页面中显示
def getData1(request,data):
    s="使用str转换器，数据为：%s，类型为：%s" % (data,type(data))    
    return HttpResponse(escape(s))
def getData2(request,data):
    s="使用int转换器，数据为：%s，类型为：%s" % (data,type(data))    
    return HttpResponse(escape(s))
def getData3(request,data):
    s="使用slug转换器，数据为：%s，类型为：%s" % (data,type(data))    
    return HttpResponse(escape(s))
def getData4(request,data):
    s="使用UUID转换器，数据为：%s，类型为：%s" % (data,type(data))    
    return HttpResponse(escape(s))
def getData5(request,data):
    s="使用path转换器，数据为：%s，类型为：%s" % (data,type(data))    
    return HttpResponse(escape(s))

def getReData(request,data):   
    return HttpResponse("使用正则表达式中嵌套的参数data：%s" % (data))

def getExtraData(request,data,ex):
    return HttpResponse("从URL获取的数据：%s，附加数据：%s" % (data,ex))

def useDefault(request,data=123):
    return HttpResponse("使用带默认值的参数data=123，当前值：%s" % (data))

from django.urls import reverse
def getUrlNoPara(request):
    return HttpResponse("请求的URL路径为：%s" % reverse("urlNoPara"))

def getUrlArgs(request,data):
    return HttpResponse("请求的URL路径为：%s" % reverse("UrlArgs",args=['abcd']))
def getUrlKwargs(request,data):
    return HttpResponse("请求的URL路径为：%s" % reverse("UrlKwargs",kwargs={'data': 1234}))

def getViewUrl(request):
    return HttpResponse("getUrlKwargs请求的URL路径为：%s" % \
                                  reverse(getUrlKwargs,kwargs={'data': 1234}))

from django.shortcuts import render
def reverseInTemplates(request,data):
    return render(request,'showurl.html',{'data':data})

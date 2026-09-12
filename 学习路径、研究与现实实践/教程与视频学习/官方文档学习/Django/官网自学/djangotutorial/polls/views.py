from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("你好世界。您位于民意调查索引处。")


def detail(request, question_id):
    return HttpResponse("您正在查看问题 %s。" % question_id)


def results(request, question_id):
    response = "您正在查看问题 %s 的结果。"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("您正在对问题 %s 进行投票。" % question_id)
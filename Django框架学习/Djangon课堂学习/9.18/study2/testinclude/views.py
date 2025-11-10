from django.http import HttpResponse
def useinclude(request):
    return HttpResponse('这是应用testinclude中的视图函数useinclude的响应')


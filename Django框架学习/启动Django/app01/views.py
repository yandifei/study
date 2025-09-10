import markdown
from django.shortcuts import render, HttpResponse
import markdown

# Create your views here.
# 自我研究
def init(request):
    # 读取html
    with open("./笔记.md", "r", encoding="utf-8") as f:
        text = f.read()
    # 把我的markdown文本转换为 HTML
    html_content = markdown.markdown(text)
    # 将转换后的html内容传递给模板
    return HttpResponse(html_content)

# 这个函数默认需要一个参数request
def index(request):
    return HttpResponse("欢迎使用")

# 用户列表
def user_list(request):
    return HttpResponse("用户列表")

# 添加用户
def user_add(request):
    return HttpResponse("添加用户")

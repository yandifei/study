"""
URL configuration for study project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 内置库
import datetime

# 第三方库
from django.contrib import admin
from django.urls import path, register_converter, re_path
# 自己的库
from app1 import views as app1_views
from example import views as ex
from example.converter import MyConverter


urlpatterns = [
    path("admin/", admin.site.urls, name="管理员界面"),  # 这里默认是Django界面
    path("index", app1_views.index, name="首页"),
    path(f"{datetime.date.today().year}/{datetime.date.today().month}/{datetime.date.today().day}",
         app1_views.get_time, name="年/月/日"),
    # http://localhost:8000/爱丽丝/666/3a352e31-9f33-42d2-895d-fedb99640995/111
    path("<str:str1>/<int:int1>/<uuid:uuid1>/<path:path1>", app1_views.test, name="路由转换器"),
    # # 自定义路由（手机号）（http://127.0.0.1:8000/mobile/13812345678/）
    # path('mobile/<mobile:phone_num>/', ex.show_mobile),
    # 老师教的的手机号正则（必须加个括号）（http://127.0.0.1:8000/mobile/13812345678/）
    re_path(r"^mobile/(1[3-9]\d{9})/$", ex.show_mobile),
    # 老师的年展示年（http://127.0.0.1:8000/articles/2025/）
    re_path(r"^articles/(?P<year>[0-9]{4})/$", ex.show_year),
    # 老师的年展示年月（http://127.0.0.1:8000/articles/2025/12/）
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[1-9]|1[0-2])/$",ex.show_year_month),
    # 合理匹配规则（4个数字0-9，12个月份）
    # re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[1-9]|1[0-2])/$",views.show_year_month)
    # re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>([1-9]|1[0-2]))/$",ex.show_year_month),
    # 我的邮箱正则匹配
    re_path(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", ex.show_mail)
]

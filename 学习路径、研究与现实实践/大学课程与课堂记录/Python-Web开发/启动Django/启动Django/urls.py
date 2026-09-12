"""
URL configuration for 启动Django project.

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

from django.contrib import admin
from django.urls import path

# 导入自己写的的views
from app01 import views

urlpatterns = [
    # 不用自带的
    # path("admin/", admin.site.urls),
    # 自我研究
    path("", views.init),

    # 主页，xxx.com/index/ -> 函数
    path("index/", views.index),
    # 用户列表
    path("user/list", views.user_list),
    # 添加用户
    path("user/list", views.user_add),
]

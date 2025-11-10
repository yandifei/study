"""
URL configuration for chapter02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from example.converter import MyConverter
from example import views
urlpatterns = [
    path('mobile/<mobile:phone_num>/', views.show_mobile),
    #  添加一个匹配根路径 / 的模式，将其指向 views.index
    path('', views.index, name='index')
]
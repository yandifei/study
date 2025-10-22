#chapter3\useAppNameSpace\urls.py
from django.urls import path
from . import views
app_name="myAppUrlNamespace"  #定义网址的应用命名空间，先注释掉，以便测试
urlpatterns = [
    path('', views.index,name="Default"), 
    path('<data>/', views.index,name="nData"), 
]
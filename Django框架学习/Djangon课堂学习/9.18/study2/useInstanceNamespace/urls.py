#chapter3\useInstanceNamespace\urls.py
from django.urls import path
from . import views
app_name="myAppSpace"  #定义应用命名空间
urlpatterns = [
    path('', views.index,name="Default"), 
    path('<data>/', views.index,name="nData"), 
]
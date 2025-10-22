from django.urls import path
from app01 import views
app_name = 'app01'
urlpatterns = [
    path('index/', views.url_path, name='url_path'),
]

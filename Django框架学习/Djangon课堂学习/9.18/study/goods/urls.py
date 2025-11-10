from django.urls import path
from goods import views
app_name = 'goods'
urlpatterns = [
    path('url-reverse/', views.get_url, name='url'),
    path('index/', views.index, name='index'),
]

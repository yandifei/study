from django.urls import path, re_path
from users import views
app_name = 'users'
urlpatterns = [
    path('login/', views.login),
    path('blog-list/', views.blog, {'blog_id': 3}),
    path('book/', views.book),
    path('column/', views.column),
    path('index/', views.index, name='index'),
]

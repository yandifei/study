#chapter3\testinclude\urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('sub/',views.useinclude), 
   
]
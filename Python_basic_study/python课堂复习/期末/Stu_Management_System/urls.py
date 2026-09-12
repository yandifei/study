"""
URL configuration for Stu_Management_System project.

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
from student_manager import views as stu_views

# urls.py

urlpatterns = [
    path("admin/", admin.site.urls),
    path('students/', stu_views.student_list, name='student_list'),

    # 【必须放在前面】具体的添加页面路径
    path('students/add/', stu_views.add_student, name='add_student'),

    # 【必须放在后面】动态匹配 ID 的路径
    path('students/<str:stu_id>/', stu_views.student_detail, name='student_detail'),

    path('students/<str:stu_id>/add_score/', stu_views.add_score, name='add_score'),
]
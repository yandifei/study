# course_manager/views.py
from django.shortcuts import render
from django.http import JsonResponse
from student_manager.models import Student
from .models import CourseScore


def add_or_update_score(request):
    if request.method == "POST":
        sid = request.POST.get('stu_id')
        c_name = request.POST.get('course_name')
        c_score = request.POST.get('score')

        student = Student.objects.get(stu_id=sid)

        # 核心逻辑：模拟字典赋值
        obj, created = CourseScore.objects.update_or_create(
            student=student,
            course_name=c_name,
            defaults={'score': c_score}
        )

        return JsonResponse({"status": "success", "action": "created" if created else "updated"})

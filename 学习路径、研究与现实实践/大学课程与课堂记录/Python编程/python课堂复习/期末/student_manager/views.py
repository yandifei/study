from django.shortcuts import render, redirect, get_object_or_404
# student_manager/views.py
from .models import Student
from .forms import StudentForm, ScoreForm

def student_list(request):
    # 获取所有学生对象
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})


def student_detail(request, stu_id):
    # 根据学号获取学生，不存在则返回404
    student = get_object_or_404(Student, stu_id=stu_id)

    # 获取该生所有成绩 (利用 related_name)
    scores = student.scores.all()

    return render(request, 'students/detail.html', {
        'student': student,
        'scores': scores
    })




# 添加学生
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

# 给特定学生添加成绩
def add_score(request, stu_id):
    student = Student.objects.get(stu_id=stu_id)
    if request.method == "POST":
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_obj = form.save(commit=False)
            score_obj.student = student  # 关联到当前学生
            score_obj.save()
            return redirect('student_detail', stu_id=stu_id)
    else:
        form = ScoreForm()
    return render(request, 'students/score_form.html', {'form': form, 'student': student})
from django import forms
from .models import Student
from score_manager.models import CourseScore

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['stu_id', 'name', 'sex', 'age']
        # 为 Bootstrap 添加样式类
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'})
            for field in ['stu_id', 'name']
        }

class ScoreForm(forms.ModelForm):
    class Meta:
        model = CourseScore
        fields = ['course_name', 'score']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# 学生模型
from student_manager.models import Student


class CourseScore(models.Model):
    # 映射原代码中的 self.course 字典结构
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name="所属学生"
    )
    course_name = models.CharField(max_length=100, verbose_name="课程名",)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],verbose_name="分数")

    class Meta:
        # 模拟原代码中字典键的唯一性：同一个学生每一科只有一个分数
        unique_together = ('student', 'course_name')

    def __str__(self):
        return f"{self.course_name}: {self.score}"
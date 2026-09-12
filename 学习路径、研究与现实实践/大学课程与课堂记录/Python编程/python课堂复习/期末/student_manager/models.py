from django.db import models

class Student(models.Model):
    # 映射 id：在 Django 中通常建议使用自动递增的主键，
    stu_id = models.CharField(max_length=20, primary_key=True, verbose_name="学号")

    # 映射 name, sex, age
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.CharField(max_length=10,choices=[('M', '男'),('F', '女'),('U', '未知'),], verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")

    def get_average_score(self):
        # 聚合查询该生所有成绩的平均值
        avg = self.scores.aggregate(Avg('score'))['score__avg']
        return round(avg, 2) if avg else 0

    def __str__(self):
        return f"{self.stu_id} - {self.name}"


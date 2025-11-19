from django.db import models

# ====================================================================
# 1. Question 模型（问题）
# ====================================================================
class Question(models.Model):
    # 'question_text' 字段用于存储问题的内容。
    # CharField 适用于短字符串。
    # max_length=200 限制了问题文本的最大长度为 200 个字符。
    question_text = models.CharField(max_length=200)

    # 'pub_date' 字段用于存储问题的发布日期和时间。
    # DateTimeField 用于日期和时间数据。
    # "date published" 是可选的人类可读名称，用于管理界面等地方显示。
    pub_date = models.DateTimeField("date published")

# ====================================================================
# 2. Choice 模型（选项）
# ====================================================================
class Choice(models.Model):
    # 'question' 字段是连接到 Question 模型的关键。
    # ForeignKey 定义了多对一关系：一个 Question 可以有多个 Choice，但一个 Choice 只属于一个 Question。
    # on_delete=models.CASCADE 意味着如果引用的 Question 被删除，所有关联的 Choice 也会被自动删除（级联删除）。
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # 'choice_text' 字段用于存储每个选项的内容。
    choice_text = models.CharField(max_length=200)

    # 'votes' 字段用于存储该选项获得的票数。
    # IntegerField 用于存储整数值。
    # default=0 设置了新创建的选项的票数默认为 0。
    votes = models.IntegerField(default=0)
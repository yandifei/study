<center>
    <h1>学生管理系统</h1>
</center>

# 引言
这个其实就是加东西，堆积木一样，`Stu_Management_System.py`是老师给的源文件
- 增加数据库
- 打包成独立的exe
- 增加UI交互界面

用PyQt画界面太累了，还是上HTML吧

# Stu_Management_System.py源码解析
`StuManagementSystem`
`Student`
`主业务逻辑(while True)`

## 业务输出
```
print("| 1 添加学生或者添加课程     |")
print("| 2 删除学生及对应的课程     |")
print("| 3 修改学生的基本信息       |")
print("| 4 查询信息                 |")
print("| 5 退出学生管理系统         |")
```
老师增加的要求：打开下列学生管理系统，丰富其功能（包括不限于年龄、分数的校验，新增成绩管理功能：修改分数、删除课程、计算学生总分平均分，信息存储等功）


功能需求分类
- 对学生的增删改查
- 对成绩的增删改查
- 对数据进行校验

# 数据库
为了可移动的打包放弃mysql，直接用轻量级的sqlite

# 学生数据模型设计
原来的代码
```python
self.id = id
self.name = name
self.sex = 
self.age = age
self.course = {}
```
直接迁移到`student_manager/models.py`目录下的`class Student(models.Model):`和`class CourseScore(models.Model):`。其中`CourseScore`里面有

## 属性限制
`id`主键
`name`长度最多为50，防止英文名太长
`sex`仅能选'男','女','未知'
`age`没有限制
`course`单独拎出来做个app


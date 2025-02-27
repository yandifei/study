# 类、对象（属性、方法）、构造方法学习
"""
开学了有一批学生信息需要录入系统，请设计一个类，记录学生的:姓名、年龄、地址，这3类信息
请实现:
通过for循环，配合input输入语句，并使用构造方法，完成学生信息的键盘录入
输入完成后，使用print语句，完成信息的输出
"""
class Student:
    def __init__(self, num, name, age, address):
        self.num = num
        self.name = name
        self.age = age
        self.address = address
        print(f"学生{self.num}信息录入完成，信息为：【学生姓名：{self.name}，年龄：{self.age}，地址：{self.address}】,")

# student_list =[]
# for i in range(1,11):
#     print(f"当前录入第{i}位学生信息，总共需录入10位学生的信息")
#     i = Student(i, input("请输入学生姓名："), int(input("请输入学生年龄：")), input("请输入学生地址："))

class Student2:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"name{self.name}, age{self.age}"

    def __lt__(self, other):
        return self.age > other.age

yandifei1 = Student2("雁低飞", 21)
yandifei2 = Student2("yandifei", 30)
print(yandifei1 > yandifei2)









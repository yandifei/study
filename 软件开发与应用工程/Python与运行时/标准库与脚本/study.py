"""
print("hello world")
print("helo world")

# 开始注释
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("world")
"""
# from fileinput import close
# from tkinter.font import names

# from tkinter.font import names

from time import sleep

# 字符串拼接
"""
print("hello"+"world")
"""
# 格式化拼接
# age = 22
# print("我的年龄是%d" % age)
#
# # 多个格式化拼接
# age = 22
# sex = '男'
# print("我今年的年龄是%d，性别是%c" %(age,sex))

# 输入学习
# name = input("请输入你的名字？\n")
# print(f"你的名字是{name}")
# num = input("请输入你的手机密码\n")
# num = int(num)
# print("你的手机密码类型是：",type(num))
# print(f"你的手机密码是：{num}")

# age = 30
# if age == 30:
#     print("年龄是30")

# 练习
# print("欢迎来到雁低飞的的儿童游乐园，儿童免费，成人收费")
# age = int(input("请输入你的年龄:"))
# if age >= 18:
#     print("您已成年，游玩补票需要10元。")
# else:
#     print("您是未成年，可以免费游玩")
# print("祝您游玩愉快。")

# 练习2
# print("欢迎来到雁低飞的游乐园")
# height = int(input("请输入您的身高（cm）:"))
# if height > 120:
#     print("您的身高超出120cm，游玩需要够票10元。")
# else:
#     print("您的身高未超出120cm，可以免费游玩。")
# print("祝您游玩愉快")

# 练习3
# a = int(input("请输入第一个猜想的数字："))
# if a != 10:
#     a = int(input("不对，再猜一次："))
# if a != 10:
#     a = int(input("不对，再猜最后一次："))
# if a != 10:
#     print("Sorry, 全部猜错了，我想的是10")
# else:
#     print("你猜对了")

# 随机数字生成
# import random
# num = random.randint(1,10)
# print(num)

# 练习4
# import random
# rannum = random.randint(1,10)
# print(f"生成的随机数字是{rannum}")
# a = int(input("请猜一个1~10的数字："))
# if a != rannum:
#     if a > rannum:
#         print("数字太大了")
#     else:
#         print("数字太小了")
#         a = int(input("猜错了，再猜一次"))
#         if a != rannum:
#             if a > rannum:
#                 print("数字太大了")
#             else:
#                 print("数字太小了")
#                 a = int(input("猜错了，再猜最后一次"))
#                 if a == rannum:
#                     print("你猜对了")
#                 else:
#                     print(f"三次机会已经用光了，答案是{rannum}")
#         else:
#             print("你猜对了")
# else:
#     print("你猜对了")

# study
# i = 0
# while i < 100:
#     i += 1
#     print(f"开始累加，累计的数值为{i}")

# 练习5
# count = 0
# i = 1
# while i <= 100:
#     count += i
#     i += 1
# print(f"1~100累计的和为{count}")

# 练习6
# import random
# rannum = random.randint(1,100)
# print(f"生成的随机数值是：{rannum}")
# a = int(input("请输入猜测的数值：")) # 这里已经猜了一次了
# count = 1 # 记录猜测的次数，1为初始值是因为已经猜测过一次了
# while rannum != a:
#     if a > rannum:
#         a = int(input("太大了，请重猜："))
#     else:
#         a = int(input("太小了，请重猜："))
#     count += 1
# print(f"恭喜你猜对了，总共猜测了{count}次")

# 练习7（打印9X9乘法表）
# print("乘法口诀表")
# i = 0
# while i != 10:
#     j = 0
#     while i != j:
#         j += 1
#         print(f"{j}*{i}={i * j}\t", end='')
#     print("\n")# 打印完一行后自动换行
#     i += 1

#study
# for x in "name":
#     print(x)

# 练习8
# count = 0
# for i in "itheima is a brand of itcast":
#     if i == 'a':
#         count += 1
# print("itheima is a brand of itcast，共有%d个a" % count)

# 练习9
# count = 0
# for i in range(int(input("请输入一个小于100的数字：")), 101):
#     if i % 2 == 0:
#         count += 1
# print(f"共有{count}个偶数")

# 练习10
# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f"{j}*{i}={i*j}\t",end='')
#     print()

# 练习11
# 方法一
# import random
# account_balance = 10000
# for i in range(1,21):
#     performance_score = random.randint(1, 10)
#     if performance_score < 5:
#         print(f"员工{i}，绩效点{performance_score}，低于5，不发工资，下一位。")
#         continue
#     if account_balance == 0:
#         print(f"账户余额不足，账户余额为:{account_balance}")
#         break
#     account_balance -= 1000
#     print(f"向员工{i}发放工资1000元，账户余额{account_balance}。")
# 方法二
# import random
# for i in range(1,21):
#    performance_score = random.randint(1, 10)
#     if performance_score < 5:
#         print(f"员工{i}，绩效点{performance_score}，低于5，不发工资，下一位。")
#     else:
#         for j in range(0,10001,1000):
#             if 10000 != j:
#                 print(f"账户余额不足，账户余额为:{10000 - j}")
#                 break
#             print(f"向员工{i}发放工资1000元，账户余额{j}。")

# study
# def yandife():
#     print("雁低飞")
# yandife()

# 练习12
# def fever_jude(temperature):
#     print("欢迎来到广州！请出示您的健康码以及72小时核酸证明，并配合测量体温！")
#     if temperature > 37.5:
#         print(f"体温测量中，您的体温是：{temperature}度，需要隔离!")
#     else:
#         print(f"体温测量中，您的体温是：{temperature}度，体温正差请进!")
# fever_jude(float(input("请输入你的体温：")))

# 练习13（银行取款案例）
# money = 5000000
# name = "雁低飞"
# # 主菜单函数
# def menu():
#     print(f"------------------------主菜单------------------------\n{name}，您好，欢迎来到雁低飞的银行ATM。请选择操作：\n查询余额\t[输入1]\n存款\t[输入2]\n取款\t[输入3]\n退出\t[输入4]")
#     select = input("请输入您的选择：")
#     if select == "1":
#         select_money()# 查询余额
#         menu()
#     elif select == "2":
#         put_money()
#         menu()
#     elif select == "3":
#        out_money()
#        menu()
#     else:
#         print("已退出雁低飞的ATM系统")
#
# # 查询余额
# def select_money():
#     print(f"-----------------------查询余额-----------------------\n{name}，您好，您的余额剩余：{money}元")
#
# # 存款
# def put_money():
#     global money
#     input_money = int(input("请输入存款金额:"))
#     money += input_money
#     print(f"-------------------------存款-------------------------\n{name}，您好，您存款{input_money}元成功\n{name}，您好，您的余额剩余：{money}元")
#
# # 取款
# def out_money():
#     global money
#     output_money = int(input("请输入取款金额"))
#     money -= output_money
#     print(f"-------------------------取款-------------------------\n{name}，您好，您取款{output_money}元成功\n{name}，您好，您的余额剩余：{money}元")
#
# if input("请输入你的账户名字:") == "雁低飞":
#     menu()
# else:
#     print("未找到该账户名字")

# 练习14
# list_study = [21, 25, 21, 23, 22, 20]
# print(f"列表状态：{list_study}")
# list_study.append(31)
# print(f"列表状态：{list_study}")
# list_study.extend([29, 33, 30])
# print(f"列表状态：{list_study}")
# print(f"列表第一个元素：{list_study[0]}")
# print(f"列表第一个元素：{list_study[len(list_study)-1]}")
# print(f"31号元素的下标位置是{list_study.index(31)}")

# 练习15(列表练习)
# mylist = [1,2,3,4,5,6,7,8,9,10]
# print(f"初始数组为{mylist}")
# # while遍历
# while_list = []
# index = 0
# while index < len(mylist):
#     if mylist[index] % 2 == 0:
#         while_list.append(mylist[index])
#     index += 1
# print(f"while遍历存储偶数的数组为{while_list}")
# # for遍历
# for_list = []
# for i in mylist:
#     if i % 2 == 0:
#         for_list.append(i)
# print(f"for遍历存储偶数的数组为{for_list}")

# 练习16(元组练习)
# mytuple = ("雁低飞", 11, ["football", "music"])
# print(f"年龄的下标是{mytuple.index(11)}")
# print(f"学生的姓名是{mytuple[0]}")
# mytuple[2].remove("football")
# print(f"元组的状态{mytuple}")
# mytuple[2].append("coding")
# print(f"元组的状态{mytuple}")

# 练习17(字符串练习)
# print(f"字符串itheima itcast boxuegu中有:{"itheima itcast boxuegu".count("it")}个it字符")
# print(f"字符串itheima itcast boxuegu，被替换空格后，结果：{"itheima itcast boxuegu".replace(" ", "|")}")
# print(f"字符串itheima itcast boxuegu，按照|分割后，得到：{"itheima itcast boxuegu".replace(" ", "|").split("|")}")

# 练习18(切片练习)
# print(f"把\"万过薪月，员序程马黑来，nohtyP学\"切片后得到：{"万过薪月，员序程马黑来，nohtyP学"[::-1].replace("来", "").split("，")[1]}")

# 练习19(集合练习（去重）)
# my_list =['黑马程序员','传智播客','黑马程序员','传智播客','itheima','itcast','itheima','itcast','best']
# new_list = set()
# for i in my_list:
#     new_list.add(i) # 添加集合元素
# print(f"去重后的集合为{new_list}")
# # 一句话秒了
# print(f"有列表：['黑马程序员','传智播客','黑马程序员','传智播客','itheima','itcast','itheima','itcast','best']存入集合后的结果：{ {'黑马程序员','传智播客','黑马程序员','传智播客','itheima','itcast','itheima','itcast','best'}}")

# 练习20(字典练习)
# employee_table = {"王力鸿": {
#     "部门": "科技部",
#     "工资": 3000,
#     "级别": 1
# }, "周杰伦": {
#     "部门": "市场部",
#     "工资": 5000,
#     "级别": 2,
# }, "林俊杰": {
#     "部门": "市场部",
#     "工资": 7000,
#     "级别": 3,
# }, "张学友": {
#     "部门": "科技部",
#     "工资": 4000,
#     "级别": 1,
# }, "刘德华": {
#     "部门": "市场部",
#     "工资": 6000,
#     "级别": 2,
# }}
# print(f"全体员工当前信息如下：\n{employee_table}")
# # 并通过for循环，对所有级别为1级的员工，级别上升1级，薪水增加1000元
# for i in employee_table:
#     if employee_table[i]["级别"] == 1:
#         employee_table[i]["级别"] += 1
#         employee_table[i]["工资"] += 1000
# print(f"全体员工级别为1的员工完成升值加薪操作，操作后:\n{employee_table}")

# def test(*args,**kwargs):元组，字典

#函数作为参数传递study
# def computer(x, y):
#     return x * y
#
# def data(computer):
#     result = computer(2, 4)
#     print(f"{result}")
#
# def add(x, y):
#     return x + y
#
# data(add)

# 匿名函数study（lambda更加侧重算法逻辑）
# def test_func(compute):
#     result = compute(1, 2)
#     print(f"结果是：{result}")
#
# test_func(lambda x, y : x + y) #使用一次lambda直接报废，简称一夜情

# # 文本内容相关学习
# f = open("D:\\鸣潮脚本\\Free-my-WW\\python_study.txt", "r", encoding="UTF-8")
# print(f"{type(f)}")


# 练习21(文本读取统计练习)
# print(f"记录出来文本中\"itheima\"共有{open("D:/鸣潮脚本/Free-my-WW/word.txt", "r", encoding = "UTF-8").read().count("itheima")}个")


# 文本写入研究
# a = open("D:/鸣潮脚本/Free-my-WW/word.txt", "w", encoding = "UTF-8")
# a.write("hello world") # 写入是清空重写！！！改名叫做rewrite得了
# a = open("B:\\鸣潮\\Wuthering Waves\\Wuthering Waves Game\\Wuthering Waves.exe") # 尝试打开游戏，实验结果是无法打开
def correct_path(absolute_path):
    """
    把绝对路径的"\"转换成"/"防止转义出现歧义
    :param absolute_path: 正常的绝对路径
    :return: 不怕转义错误的绝对路径
    """
    return absolute_path.replace("\\", "/")


# 练习21(文本相关操作练习)
# 把文本复制到新的文件里面去
# open("D:\\鸣潮脚本\\Free-my-WW\\bill.txt.bak", "w", encoding = "UTF-8").write(open("D:\\鸣潮脚本\\Free-my-WW\\bill.txt", "r", encoding = "UTF-8").read())
# with open("D:\\鸣潮脚本\\Free-my-WW\\bill.txt.bak", "w", encoding="UTF-8") as a:
#     for i in open("D:\\鸣潮脚本\\Free-my-WW\\bill.txt", "r", encoding = "UTF-8").readlines():
#         if i.strip().split(",")[4] == "正式":
#             a.write(i)
# print(f'筛选后得到的新的文本内容是:\n{open("D:\\鸣潮脚本\\Free-my-WW\\bill.txt.bak", "r", encoding="UTF-8").read()}')

# 异常捕获（正常来说代码出现错误的时候是直接停止的，但是异常捕获可以捕获错误的地方并且让代码继续跑下去）
"""
异常捕获可以指定某种类型的异常或多种类型的异常，其中也有捕获所有的异常（这是最顶级的，也是我认为最实用的）
"""
# 全部异常捕获（方法一）
"""
try:
    print(asdf) #可能出现异常的代码
except:
    print("出现异常")
    print()
"""
# 全部异常捕获（方法二），可以反馈错误具体在哪
# try:
#     name #异常代码
# except Exception as e:  # 这个e是可以自己改变的，a或其他字符都可以
#     print("出现异常了")
#     print(e)    # 异常具体地方和原因
# else:
#     print("代码没有异常时执行")
# finally:
#     print("无论代码是否有异常都得执行")

# 导入学习
    # 使用import导入
""""
import time # 导入time这个模块，其中有很多功能，可以通过.来调用time的方法，如time.sleep
"""
    # 使用* 导入time模块的全部功能，这个是直接导入模块time里面的功能全部导入，不导入整个模块
"""
from time import *
print("你好")
sleep(5)
print("我好")
"""
#*表示全部的意思
    # 改变某个模块的功能调用名称
""""
from time import sleep as sl    # 把time模块中的sleep功能改名为sl，可以通过sl直接调用该time模块中的sleep功能
print("你好")
sl(5)
"""

# 自定义模块包
"""
就是创建一个.py的文件正常的写代码就可以了，需要使用的时候导入就可以了
"""
# if __name__ == '__main__':    #这个函数用于对模块文件的测试，导入后不会对该代码块的内容有任何影响

"""
__all__ = ["函数名字"]
这个函数是当我们使用form 模块名 import * 时只能导入给定的函数。注：函数名字要有双引号，如果指定导入__all__ = ["函数名字"]
里面的"函数名字" ，那么是可以破除限制的 
"""

# 安装第三方包
"""
1.
    在命令提示符内:
    pip install 包名称
    pip install -i
    https://pypi.tuna.tsinghua.edu.cn/simple 包名称
2. 
    在pycharm里面的右下角，倒数第二个图标点击后有管理软件包的图标，点击即可，自己搜索需要的包，
    当然默认是外国了网络，我还没有找到在自己的pycharm换源的方法
"""

# # json学习
# import json # 导入json的包（自带的）
"""
其实json格式就是python里面的字典或者是列表里面嵌套的字典
josn是一种轻量级的数据交互格式，采用完全独立于编程语言的文本
它的作用是提供不同计算机编程语言的数据交互
# 中文直接输出会被标准翻译为ascii导致乱码
# ensure_ascii=False这个代码是不转换为美国国际标准的ascii码，直接输出
"""
# 字典转换为json格式
# data = {"yandifei":1000,"雁低飞":1001,"燕子":1010,"雁子":1011}
# print(data)
# data = json.dumps(data, ensure_ascii=False)
# print(data)
# # 把json数据转化为python的列表或字典
# json_data = '[{"name": "张大山", "age": 11},{"name": "王大锤", "age": 13},{"name": "赵小虎", "age": 16}]'
# need_data = json.loads(json_data)
# print(need_data)

# 数据可视化学习
# from pyecharts.charts import Line # 导入折线图的功能函数
# from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, VisualMapOpts # 导入全局配置项功能函数
# # 创建一个折线图对象
# line = Line()
# # x轴添加数据
# line.add_xaxis(["中国", "美国", "英国"])
# # y轴添加数据
# line.add_yaxis("GDP", [30, 20, 10])
# # 添加额外功能
# line.set_global_opts(
#     title_opts=TitleOpts(title="GDP展示", pos_left="center", pos_bottom="1%"),
#     legend_opts=LegendOpts(is_show=True),
#     toolbox_opts=ToolboxOpts(is_show=True),
#     visualmap_opts=VisualMapOpts(is_show=True)
# )
#
# # 生成图表(网页格式的)
# line.render()
# # 生成图表(图片格式的)
# # line.render_notebook()

# 类学习
"""
类好比是一张设计图纸，对象就是根据设计图纸制造出来的
对象可以有很多个，但都是根据设计图纸制作出来的
类这个设计图纸有设计的属性和他的功能，如闹钟设计图纸，
闹钟设计图纸中有制作闹钟长度、高度、材质等等这些都是属性
，称为成员属性。闹钟设计图纸还包括了他的响铃功能，这被成为
成员方法
"""
# class Person:
#     # name = None
#     # age = None
#     # tel = None
#     def __init__(self, name, age, tel):
#         self.name = name
#         self.age = age
#         self.tel = tel
#         print(f"创建了姓名为：{self.name}，年龄为：{self.age}，身高为：{self.tel}的对象")
#
#
# yandifei = Person("雁低飞", 21, 12)
# yandifei.age += 1
# # yandifei.tel += 1
# print(yandifei.age)

# a = None
# if  not a:
#     # a += 1
#     print(f"{a}")

# f = open("D:\\鸣潮脚本\Free-my-WW\\bill.txt", "r", encoding="UTF-8")
# print(f.read())



































































































































































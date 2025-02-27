# 这里的数据调用是用之前类对象的方法， 这里是定义类和方法
#数据库综合练习
"""
读取文本和json文本，分割去除没用的数据提取需要的数据
链接数据库，使用python来进行数据库表格的创建
对数据进行增删改查询
练习过程要
全程使用面向对象的思想
                    数据文件路径
D:/Python_study/练习案例用到的数据（黑马）/2011年1月销售数据.txt
D:/Python_study/练习案例用到的数据（黑马）/2011年2月销售数据JSON.txt
"""
# 导入自定义类的宏包
from get_data import *
from view_class import *    # 图形可视化的宏包
from sql_oriented import *  # 导入自定义的数据库的宏包（内置数据库函数）
# 开始计算统计
txt_file_reader = TextFileRead("D:/Python_study/练习案例用到的数据（黑马）/2011年1月销售数据.txt")
json_file_reader = JsonFileRead("D:/Python_study/练习案例用到的数据（黑马）/2011年2月销售数据JSON.txt")

jan_data : list[SplitData] = txt_file_reader.read_data()
feb_data : list[SplitData] = json_file_reader.read_data()
# 将2个月份的数据合并成一个list数据来存储
all_data = jan_data + feb_data
data_dict = dict()  #定义空字典
for i in all_data:
    if i.date in data_dict.keys():  #判断字典里面是否有日期存在
        data_dict[i.date]  += i.money    # 累加金额
    else:   #字典里面没有该日期则添加日期
        data_dict[i.date] = i.money #添加该日期的字典和该日期的金额数据

# print(data_dict.values())
#调用类创捷柱状图表
money_view = CreateBar(data_dict.keys(),data_dict.values())   #创建自定义图表的类对象
money_view.create_bar()     # 调用方法生成每日金额销售柱状图

# SQL数据操作相关
#调用自定义的sql函数（连接、建立数据库、建立表格、输入数据、断开连接）
databases_insert(all_data)  # 直接调用函数插入数据
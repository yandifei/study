# 构建类、对象和方法(文件读取和数据转换)
""" 数据文件路径
D:/Python_study/练习案例用到的数据（黑马）/2011年1月销售数据.txt
D:/Python_study/练习案例用到的数据（黑马）/2011年2月销售数据JSON.txt
"""
# import json
# 需要导入的包
from json import * # 导入json的包用来转换json数据
from os.path import split


# 读取普通文本读数据

# 构建一个大的类（标准）
class File:
    pass

# 定义抽象类来做不同文件数据读取的顶层设计，确定有哪些功能需要实现
class FileDataRead(File):
    def read_data(self): # -> list[SplitData]:
        """读入不同形式的数据，并对数据做出处理以list的形式返回"""
        pass

# 普通文本数据读取的具体实现
class TextFileRead(FileDataRead):
    def __init__(self, txt_path):   #定义成员变量，记录普通文本文件的路径
        self.txt_path = txt_path

    # 复写，具体实现普通文本文件数据读取的方法
    def read_data(self): # -> list[SplitData]:
        need_data_list = []
        with open(self.txt_path, "r", encoding="UTF-8") as txt_read_data_oriented:
             for line in txt_read_data_oriented.readlines():
                 line_data = line.strip()   # 去掉每一行的回车符

                 line_data_list = line_data.split(",")   #使用，切割数据(获得单行数据的列表)
                 # 调用统计计算过数据的对象
                 split_data = SplitData(line_data_list[0], line_data_list[1], int(line_data_list[2]), line_data_list[3])
                 need_data_list.append(split_data)   # 将统计计算好的的数据传入列表里面
        return need_data_list

# json问本数据读取的具体实现
class JsonFileRead(FileDataRead):
    def __init__(self, json_path):  # 定义成员变量，记录json文本文件的路径
        self.json_path = json_path

    # 复写，具体实现json文本文件数据读取的方法
    def read_data(self): # -> list[SplitData]:
        need_data_list = []     # 设置一个空的列表用来存放解析后的数据
        with open(self.json_path, "r", encoding="UTF-8") as json_read_data_oriented:
            for line in json_read_data_oriented.readlines(): # 读入文件里面的json文本
                txt_data_dict = loads(line)# 将读到的每条json内容转化为txt文本(直接使用字典强制类型转换会舍弃部分内容导致导致报错)
                need_data = SplitData(txt_data_dict["date"], txt_data_dict["order_id"], int(txt_data_dict["money"]), txt_data_dict["province"])
                need_data_list.append(need_data)   # 将需要的数据添加到列表中
        return need_data_list   # 返回需要的数据数组



# 对获取的数据进行计算统计处理
class SplitData:
    def __init__(self, date, order_id, money, province):
        self.date = date            # 订单日期
        self.order_id = order_id    # 订单ID
        self.money = money          # 订单金额
        self.province = province    # 销售省份

    def __str__(self):  #确保返回的是字符串而不是地址
        return f"{self.date}, {self.order_id}, {self.money}, {self.province}"
if __name__ == '__main__':
    a = TextFileRead("D:/Python_study/练习案例用到的数据（黑马）/2011年1月销售数据.txt")
    a_list = a.read_data()
    for i in a_list:
        print(i)

    b = JsonFileRead("D:/Python_study/练习案例用到的数据（黑马）/2011年2月销售数据JSON.txt")
    b_list = b.read_data()
    for i in b_list:
        print(i)















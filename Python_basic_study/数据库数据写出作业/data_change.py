# 构建数据处理的类和方法
"""
输入数据库返回的值，对返回的值做处理
方便把文本格转换为json的格式
"""
import json
from json import * # 导入json的包
class DataModification:   # 数据修改
    def __init__(self, data):   # 输入数据库转换的数据
        self.data = data

    #对字符串进行处理修改以列表形式返回
    def data_modification(self):
        data_list = [] # 定义空列表存放全部json数据
        data_output_dict = dict()  # 定义一个空字典用来存放对应格式的数据
        for oneline in self.data:  # 把数据一行一行读出
            oneline_processing = str(list(oneline))  # 强制类型转换（元组的数据无法修改）
            oneline_processing = oneline_processing.replace("[datetime.date(", "")  # 转为开头不需要的替换为空(“[datetime.date(”)
            oneline_processing = oneline_processing.replace("]", "")  # 最后的“[”替换为空（这里不适合替换为\n）
            oneline_processing_list = oneline_processing.split(")")  # 使用分割替补日期
            oneline_processing_date = oneline_processing_list[0].replace(", ", "-")  # 将日期里面的“,”替补成“-”
            oneline_processing = oneline_processing_date + oneline_processing_list[1]  # 替补完成
            oneline_processing = oneline_processing.split(", ")  # 以“, ”分割文本获得数据来录入字典
            # print(oneline_processing)
            data_output_dict["data"] = oneline_processing[0]    # 添加日期键值对
            data_output_dict["order_id"] = oneline_processing[1]# 添加ID键值对
            data_output_dict["money"] = oneline_processing[2]   # 添加金额键值对
            data_output_dict["province"] = oneline_processing[3]# 添加省份键值对
            # data_json = json(ensure_ascii=False)
            # print(json.dumps(data_output_dict))
            data_list.append(str(data_output_dict))  # 添加字典到列表里面
        # print(data_list)
        return data_list    # 返回列表表示

#     # def input_data_dic(self):   # 将数据放入字典
#
#
#
# class DataElement(): # 不同的数据元素类(分割单行数据获取的不同字段的元素)
#     def __init__(self, date, order_id, money, province):
#         self.date = date
#         self.order_id= order_id
#         self.money =money
#         self.province = province
#
#     def __str__(self):  # 返回字符串
#         return f"{self.date}, {self.order_id}, {self.money}, {self.province}"






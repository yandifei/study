# 视图学习
from json import *
from pyecharts.charts import Line
from pyecharts.options import *
us_data_c = open("D:\\Python_study\\折线图数据\\美国.txt", "r", encoding="UTF-8")
us_data = loads(us_data_c.read().replace("jsonp_1629344292311_69436(","")[:-2])["data"][0]["trend"]
x_us_data = us_data["updateDate"][:314]
y_us_data = us_data["list"][0]["data"][:314]

ja_data_c = open("D:\\Python_study\\折线图数据\\日本.txt", "r", encoding="UTF-8")
ja_data = loads(ja_data_c.read().replace("jsonp_1629350871167_29498(","")[:-2])["data"][0]["trend"]
x_ja_data = ja_data["updateDate"][:314]
y_ja_data = ja_data["list"][0]["data"][:314]
#
in_data_c = open("D:\\Python_study\\折线图数据\\印度.txt", "r", encoding="UTF-8")
in_data = loads(in_data_c.read().replace("jsonp_1629350745930_63180(","")[:-2])["data"][0]["trend"]
x_in_data = in_data["updateDate"][:314]
y_in_data = in_data["list"][0]["data"][:314]

# 生成图表
line = Line()
# 录入x轴的数据
line.add_xaxis(x_us_data)
# 录入y轴的数据
line.add_yaxis("美国确诊人数",y_us_data, label_opts=LabelOpts(is_show=False))# 不在折线上显示数据
line.add_yaxis("日本确诊人数",y_ja_data, label_opts=LabelOpts(is_show=False))# 不在折线上显示数据
line.add_yaxis("印度确诊人数",y_in_data, label_opts=LabelOpts(is_show=False))# 不在折线上显示数据
# 全局配置（更好看）
line.set_global_opts(
    title_opts=TitleOpts(title="2020美日印三国确诊人数对比折线图", pos_left="center",pos_bottom="1%")
)

# 调用render方法生成图表
line.render()
# 关闭获取数据的文件
us_data_c.close()
ja_data_c.close()
in_data_c.close()

# print(us_data)
# print(ja_data)
# print(in_data)


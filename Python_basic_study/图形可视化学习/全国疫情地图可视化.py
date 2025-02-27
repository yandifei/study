# 疫情地图可视化操作
import json
from pyecharts.charts import *
from pyecharts.options import *
f = open("D:\\Python_study\\地图数据\\疫情.txt", "r", encoding="UTF-8")
data = f.read()     # 读取所有数据
f.close()       #关闭文本
data_dict = json.loads(data)    # 转换json文本为字典列表
data_list = []  # 画图用到的数据
province_data_list = data_dict["areaTree"][0]["children"]   #获得需要的
for province_data in province_data_list:
    # 要补齐省这个字和区这个字
    province_name = province_data["name"]  # 省份名称(没有加工补齐)
    if province_data["name"] == "新疆":
        province_name = province_data["name"] + "维吾尔自治区"
    elif province_data["name"] == "西藏":
        province_name = province_data["name"] + "自治区"
    elif province_data["name"] == "宁夏":
        province_name = province_data["name"] + "回族自治区"
    elif province_data["name"] == "内蒙古":
        province_name = province_data["name"] + "自治区"
    elif province_data["name"] == "广西":
        province_name = province_data["name"] + "壮族自治区"
    elif province_data["name"] == "香港":
        province_name = province_data["name"] + "香港特别行政区"
    elif province_data["name"] == "澳门":
        province_name = province_data["name"] + "特别行政区"
    elif province_data["name"] == "北京":
        province_name = province_data["name"] + "市"
    elif province_data["name"] == "天津":
        province_name = province_data["name"] + "市"
    elif province_data["name"] == "重庆":
        province_name = province_data["name"] + "市"
    else:
        province_name = province_data["name"] + "省"
    print(province_name)
    province_confirm = province_data["total"]["confirm"]  # 确诊人数
    data_list.append((province_name, province_confirm))
# print(data_list)
# 构建地图对象
map = Map()
# 添加数据
map.add("各省份的确诊人数", data_list, "china")
# 设置全局选择
map.set_global_opts(
    title_opts=TitleOpts(title="全国疫情地图"),
    visualmap_opts=VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        pieces=[
            {"min": 1, "max": 999, "lable": "1~99", "color": "#CCFFFF"},
            {"min": 100, "max": 999, "lable": "100~999", "color": "#FFFF99"},
            {"min": 1000, "max": 4999, "lable": "1000~4999", "color": "#FF9966"},
            {"min": 5000, "max": 9999, "lable": "5000~9999", "color": "#FF6666"},
            {"min": 10000, "max": 99999, "lable": "10000~99999", "color": "#CC3333"},
            {"min": 100000, "lable": "100000+", "color": "#990033"},
        ]
    )
)
# 绘制地图
map.render("全国疫情地图.html")




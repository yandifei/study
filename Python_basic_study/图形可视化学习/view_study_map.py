# 地图构建学习
# 导入需要的包
from pyecharts.charts import *
from pyecharts.options import *
# 准备地图对象
map = Map()
# 准备地图数据
data = [
    ("北京省", 99),
    ("上海省", 199),
    ("湖南省", 299),
    ("台湾省", 399),
    ("广东省", 499),
]
# 添加地图数据
map.add("测试地图", data, "china")
# 设置全局配置
map.set_global_opts(
    visualmap_opts=VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        pieces=[
            {"min": 1, "max": 9, "label": "1-9", "color": "#CCFFFF"},
            {"min": 10, "max": 99, "label": "10-99", "color": "#FF6666"},
            {"min": 100, "max": 500, "label": "100-500", "color": "#990033"}
        ]
    )
)


# 生成地图
map.render()
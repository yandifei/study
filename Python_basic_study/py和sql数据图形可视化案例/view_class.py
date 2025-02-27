# 可视化开发的类、方法定义
# 导入必要的包
from pyecharts.charts import *  # 图形构建包
from pyecharts.options import * # 可选项的包
from pyecharts.globals import * # 全局配置包
# 构建柱状图的类和方法
class CreateBar:
    def __init__(self, x, y):#构建对象的时候传入x轴和y轴的数据
        self.x = x
        self.y = y

    def create_bar(self): #成员方法
        bar = Bar(init_opts=InitOpts(theme=ThemeType.LIGHT))
        bar.add_xaxis(list(self.x))  #强制转换为list格式添加x轴数据
        bar.add_yaxis("销售额", list(self.y), label_opts=LabelOpts(is_show=False))    #强制转换为list格式添加y轴数据
        # 设置图表的全局配置
        bar.set_global_opts(
            title_opts=TitleOpts(title="每日销售额")
        )
        # 生成图表
        bar.render("每日销售额度柱状图.html")












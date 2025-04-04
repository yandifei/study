# 网页数据爬取基础学习
# 导包
from calendar import weekday
import requests     # 爬取数据的包
import re   # 正则表达式（从爬取的数据里面找到需要的数据）
"""
爬取网页文本数据，正则提取需要的数据，使用学到的文本处理方式提取需要的数据并以需要的方式返回
（要注意爬取后要进行编码转换，不然爬到的数据是乱码）
"""
url = "https://weather.cma.cn/web/weather/59287.html"   # 国家气象局的网址（测试爬广州天气）
resp = requests.get(url)    # 打开浏览器和打开网址
# 设置编码格式
resp.encoding = "UTF-8"
month_day = re.findall("<br>(.*)", resp.text) # 几月几号
weather = re.findall('<div class="day-item">\n {9}(.*)',resp.text)      # 返回星期几和天气
# print(resp.text)    # resp响应对象，对象名.属性名(返回网页代码文本)
# print(month_day)        # 日期
# print(weather)          # 天气
"""
爬取网页图片
"""
ww_logo_png_url = "https://mc.kurogames.com/static4.0/assets/logo-small-906f14d9.png"    # 鸣潮图标图片的网址
ww_logo_png = requests.get(ww_logo_png_url) # 爬取数据
# 保存到本地
with open("鸣潮图标.png", "wb") as file:
    file.write(ww_logo_png.content)


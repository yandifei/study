"""
只拿排行第几的
我要排行126的图片
"""
import io

import requests
from PIL import Image

# 必要参数
mode = "daily"  # 排行模式（daily、weekly、monthly、rookie）
# 是否r18(必须加cookie)
r18: bool = False
# 以排行为主我就得进行数据计算
rank = 600 # 排行

# # 检查是否有这个排名的插画(方法1)
# if (responds_dict := responds.json()).get("error", False):
#     print(f"没有该排名的插画")
#     exit()
# 方法2(不需要网络请求)
if rank > 500:
    print(f"没有该排名的插画")
    exit()

# 需要计算的参数
# 第几页（1页50张画）
page = (rank - 1) // 50 + 1
# 该页的具体位置
position_in_page = (rank - 1) % 50 + 1


url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={page}&format=json"
headers = { # 不带cookie无法爬取r18的数据
    # "cookie": "",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net",
}
# 请求拿到json数据
responds = requests.get(url=url,headers=headers,timeout=10)

# 目标url，但不是原图url（position_in_page - 1是因为下标的原因）
position_url = responds.json()["contents"][position_in_page - 1]["url"]
# 原图url
original_url = position_url.replace("c/480x960/", "").replace("img-master", "img-original").replace("_master1200", "")
# 原图请求
responds = requests.get(url=original_url,headers=headers,timeout=10)
if responds.status_code == 404:
    # 原图是png，更新请求链接
    png_url = original_url.replace(".jpg", ".png", 1)
    # 图片请求
    responds = requests.get(url=png_url, headers=headers, timeout=10)
# 保存转换并保存图片
with Image.open(io.BytesIO(responds.content)) as img:
    # 使用pillow实现类型转换
    img.save(f"../data/{mode}{rank}.png", "PNG")

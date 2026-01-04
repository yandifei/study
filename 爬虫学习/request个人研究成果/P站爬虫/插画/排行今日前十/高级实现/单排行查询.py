"""
我要排行126的图片
我要189和205的图片
我要r18排行101的图片和排行900的图片
"""
import io

import requests
from PIL import Image

# 必要参数
mode = "daily"  # 排行模式（daily、weekly、monthly、rookie）
# 是否r18(必须加cookie)
r18: bool = False
# 以排行为主我就得进行数据计算
rank_list = [189,205, 900, 200, 801, 1000]

# 反馈信息(用来累计)
feedback_information = ""
# 任务完成的列表
mission_complete: list[int] = []
# 超出排行的列表
over_rank: list[int] = []
# 超时的图片
over_time: list[int] = []
# 异常的图片
error_image: list[int]  = []

# 下载方法构建
def download_image(page: int, position_in_page: int):
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
        original_png_url = original_url.replace(".jpg", ".png", 1)
        # 图片请求
        responds = requests.get(url=original_png_url, headers=headers, timeout=10)
    # 保存转换并保存图片
    with Image.open(io.BytesIO(responds.content)) as img:
        # 使用pillow实现类型转换
        img.save(f"../data/{mode}{rank}.png", "PNG")


# 遍历排行列表
for rank in rank_list:
    if rank > 500:
        over_rank.append(rank)
        continue
    # 第几页（1页50张画）
    page = (rank - 1) // 50 + 1
    # 该页的具体位置
    position_in_page = (rank - 1) % 50 + 1
    try:
        download_image(page, position_in_page)
    except requests.exceptions.Timeout:
        over_time.append(rank)
    except requests.exceptions:
        error_image.append(rank)
    mission_complete.append(rank)
else:
    feedback_information += "完成任务的图片:" + "、".join(str(i) for i in mission_complete) + "。"
    if over_rank:
        feedback_information += "不存在排行的图片:" + "、".join(str(i) for i in over_rank) + "。"
    if over_time:
        feedback_information += "超时图片:" + "、".join(str(i) for i in over_time) + "。"
    if error_image:
        feedback_information += "异常图片:" + "、".join(str(i) for i in error_image) + "。"
print(feedback_information)
"""
我要从排行45-70的图片
我要r18排行前十的图片

连续的范围而不是分开的，请求速度会有极大提升
"""
import io

import requests
from PIL import Image

# 必要参数
mode = "daily"  # 排行模式（daily、weekly、monthly、rookie）
# 是否r18(必须加cookie)
r18: bool = False
# 范围(必须小到大)【1-500】
rank_start = 45
rank_end = 70

# 确保范围是从小到大
if rank_start > rank_end:
    rank_start, rank_end = rank_end, rank_start

# 确保范围有效
if 1 > rank_start or rank_end > 500:
    print("范围错误")
    exit()
# # 第几页（1页50张画）
# page = (rank - 1) // 50 + 1
# # 该页的具体位置
# position_in_page = (rank - 1) % 50 + 1

# 开始页，结束页
start_page = (rank_start - 1) // 50 + 1
end_page = (rank_end - 1) // 50 + 1
# 需要的总页数
total_pages = end_page - start_page + 1
# 起始位置（在起始页中的具体位置）
start_position = (rank_start - 1) % 50 + 1
# 结束位置（在结束页中的具体位置）
end_position = (rank_end - 1) % 50 + 1

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

# 范围在同一页
if total_pages == 0:
    url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={start_page}&format=json"
    headers = {  # 不带cookie无法爬取r18的数据
        # "cookie": "",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "referer": "https://www.pixiv.net",
    }
    # 请求拿到json数据
    responds = requests.get(url=url, headers=headers, timeout=10)
    # 切片遍历同一页下的图片(-1是因为这是下标计算)
    for content in responds.json()["contents"][start_position - 1: end_position]:
        # 原图url
        original_url = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace(
            "_master1200", "")
        try:
            # 原图请求
            responds = requests.get(url=original_url, headers=headers, timeout=10)
            if responds.status_code == 404:
                # 原图是png，更新请求链接
                original_png_url = original_url.replace(".jpg", ".png", 1)
                # 图片请求
                responds = requests.get(url=original_png_url, headers=headers, timeout=10)
            # 保存转换并保存图片
            with Image.open(io.BytesIO(responds.content)) as img:
                # 使用pillow实现类型转换
                img.save(f"../data/{mode}{content["rank"]}.png", "PNG")
        except requests.exceptions.Timeout:
            over_time.append(content["rank"])
        except requests.exceptions:
            error_image.append(content["rank"])
        mission_complete.append(content["rank"])
    else:
        feedback_information += "完成任务的图片:" + "、".join(str(i) for i in mission_complete) + "。"
        if over_rank:
            feedback_information += "不存在排行的图片:" + "、".join(str(i) for i in over_rank) + "。"
        if over_time:
            feedback_information += "超时图片:" + "、".join(str(i) for i in over_time) + "。"
        if error_image:
            feedback_information += "异常图片:" + "、".join(str(i) for i in error_image) + "。"
# 跨页
else:
    # 开始页
    url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={start_page}&format=json"
    headers = {  # 不带cookie无法爬取r18的数据
        # "cookie": "",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "referer": "https://www.pixiv.net",
    }
    # 请求拿到json数据
    responds = requests.get(url=url, headers=headers, timeout=10)
    # 切片遍历同一页下的图片(-1是因为下标)
    for content in responds.json()["contents"][start_position - 1:]:
        # 原图url
        original_url = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace(
            "_master1200", "")
        # 原图请求
        responds = requests.get(url=original_url, headers=headers, timeout=10)
        if responds.status_code == 404:
            # 原图是png，更新请求链接
            original_png_url = original_url.replace(".jpg", ".png", 1)
            # 图片请求
            responds = requests.get(url=original_png_url, headers=headers, timeout=10)
        # 保存转换并保存图片
        with Image.open(io.BytesIO(responds.content)) as img:
            # 使用pillow实现类型转换
            img.save(f"../data/{mode}{content["rank"]}.png", "PNG")

    # 中间页
    # 遍历中间页，中间可能不止一页
    for page in range(start_page - 1, end_page):
        url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={start_page}&format=json"
        headers = {  # 不带cookie无法爬取r18的数据
            # "cookie": "",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "referer": "https://www.pixiv.net",
        }
        # 请求拿到json数据
        responds = requests.get(url=url, headers=headers, timeout=10)
        # 切片遍历同一页下的图片(-1是因为下标)
        for content in responds.json()["contents"]:
            # 原图url
            original_url = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace(
                "_master1200", "")
            # 原图请求
            responds = requests.get(url=original_url, headers=headers, timeout=10)
            if responds.status_code == 404:
                # 原图是png，更新请求链接
                original_png_url = original_url.replace(".jpg", ".png", 1)
                # 图片请求
                responds = requests.get(url=original_png_url, headers=headers, timeout=10)
            # 保存转换并保存图片
            with Image.open(io.BytesIO(responds.content)) as img:
                # 使用pillow实现类型转换
                img.save(f"../data/{mode}{content["rank"]}.png", "PNG")

    # 结尾页
    url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={end_page}&format=json"
    headers = {  # 不带cookie无法爬取r18的数据
        # "cookie": "",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "referer": "https://www.pixiv.net",
    }
    # 请求拿到json数据
    responds = requests.get(url=url, headers=headers, timeout=10)
    # 切片遍历同一页下的图片(-1是因为下标)
    for content in responds.json()["contents"][: end_position]:
        # 原图url
        original_url = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace(
            "_master1200", "")
        # 原图请求
        responds = requests.get(url=original_url, headers=headers, timeout=10)
        if responds.status_code == 404:
            # 原图是png，更新请求链接
            original_png_url = original_url.replace(".jpg", ".png", 1)
            # 图片请求
            responds = requests.get(url=original_png_url, headers=headers, timeout=10)
        # 保存转换并保存图片
        with Image.open(io.BytesIO(responds.content)) as img:
            # 使用pillow实现类型转换
            img.save(f"../data/{mode}{content["rank"]}.png", "PNG")



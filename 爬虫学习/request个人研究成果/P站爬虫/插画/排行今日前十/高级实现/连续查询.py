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
rank_start = 49
rank_end = 51

save_path = "../data/"

headers = { # 不带cookie无法爬取r18的数据
    # "cookie": "",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net",
}

# --- 逻辑计算 ---
# 确保范围是从小到大
if rank_start > rank_end: rank_start, rank_end = rank_end, rank_start
# 确保范围有效
if not (1 <= rank_start <= 500 and 1 <= rank_end <= 500):
    print("范围错误"); exit()

# 开始页，结束页
start_page = (rank_start - 1) // 50 + 1
end_page = (rank_end - 1) // 50 + 1
# 反馈信息(用来累计)
feedback_information = ""
# 任务完成的列表、超时的图片、异常的图片
mission_complete, over_time, error_image = [], [], []

# --- 核心处理逻辑 --
def download_image(target_list: list):
    # 遍历下载图片
    for content in target_list:
        try:
            # 转换原图 URL (逻辑保持你的替换方案)
            original_url = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace("_master1200", "")
            # 原图请求
            responds = requests.get(url=original_url, headers=headers, timeout=10)
            if responds.status_code == 404:
                # 原图是png，更新请求链接
                png_url = original_url.replace(".jpg", ".png", 1)
                # 图片请求
                responds = requests.get(url=png_url, headers=headers, timeout=10)
            # 保存转换并保存图片
            with Image.open(io.BytesIO(responds.content)) as img:
                # 使用pillow实现类型转换
                img.save(f"{save_path}{mode}{content["rank"]}.png", "PNG")
        except requests.exceptions.Timeout:
            over_time.append(content["rank"]); continue
        except requests.exceptions:
            error_image.append(content["rank"]); continue
        mission_complete.append(content["rank"])




# 遍历页码并加载图片
for page in range(start_page, end_page + 1):
    # 请求 JSON 索引页
    url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={page}&format=json"
    responds = requests.get(url=url,headers=headers,timeout=10)
    contents = responds.json()["contents"]
    # 确定当前页需要处理的切片范围.如果是起始页，跳过前面的；如果是结束页，截断后面的
    curr_start = (rank_start - 1) % 50 if page == start_page else 0
    curr_end = (rank_end - 1) % 50 + 1 if page == end_page else 50

    target_list = contents[curr_start: curr_end]

    download_image(target_list)

# 最担心任务全失败了
if mission_complete:
    feedback_information += "完成任务的图片:" + "、".join(str(i) for i in mission_complete) + "。"
if over_time:
    feedback_information += "超时图片:" + "、".join(str(i) for i in over_time) + "。"
if error_image:
    feedback_information += "异常图片:" + "、".join(str(i) for i in error_image) + "。"
print(feedback_information)

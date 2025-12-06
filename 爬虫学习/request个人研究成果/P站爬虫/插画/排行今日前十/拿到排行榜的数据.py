"""
其实就是作品id

排行榜
json端点数据请求
https://www.pixiv.net/ajax/user/{第一个作品id}/works/latest?lang=zh
"""
import json

import requests
from bs4 import BeautifulSoup

#
url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net",
}
responds = requests.get(url=url,headers=headers,timeout=10)
# print(f"P站排行界面响应状态:{responds.status_code}")
# print(responds.text)
# 解析整个DOM
soup = BeautifulSoup(responds.text, "lxml")
# 这里面有50左右的排行数据
json = json.loads(soup.find("script", id="__NEXT_DATA__").text)
# print(f"目前排行榜共有{len(json["props"]["pageProps"]["assign"]["contents"])}张图片")
# # 遍历排行榜的作品信息
# for work_info in json["props"]["pageProps"]["assign"]["contents"]:
#     print(work_info["illust_id"])


# 内置库
import time
import json
# 第三方库
import requests
from bs4 import BeautifulSoup

num_top_images = 10     # 抓取排行前几的图片
count = 0   # 计数器，到达需要的排行就退出
url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net",


}
responds = requests.get(url=url,headers=headers,timeout=10)
print(f"P站排行界面响应状态:{responds.status_code}")
soup = BeautifulSoup(responds.text, "lxml") # 解析整个DOM
json = json.loads(soup.find("script", id="__NEXT_DATA__").text)
print(f"目前排行榜共有{len(json["props"]["pageProps"]["assign"]["contents"])}张图片")

# 遍历排行榜单的作品信息(内置id)
for artwork_info in json["props"]["pageProps"]["assign"]["contents"]:
    # json响应，真正的url在里面
    json_respond = requests.get(
        url=f"https://www.pixiv.net/ajax/illust/{artwork_info["illust_id"]}?lang=zh",headers=headers,timeout=10)
    print(f"https://www.pixiv.net/ajax/illust/{artwork_info["illust_id"]}?lang=zh") # 藏着图片url的json地址
    # # 解析json数据拿到我真正想要的(图片url)
    print(json_respond.json()["body"]["urls"]["original"])
    pic_url = json_respond.json()["body"]["urls"]["original"]
    print(json_respond.json()["body"]["urls"])
    pic_respond = requests.get(url=pic_url, headers=headers, timeout=10)
    # 图片下载保存
    with open(f"{time.time_ns()}.jpg", "wb") as pic_file:
        pic_file.write(pic_respond.content)
    count += 1
    if count == num_top_images:
        break



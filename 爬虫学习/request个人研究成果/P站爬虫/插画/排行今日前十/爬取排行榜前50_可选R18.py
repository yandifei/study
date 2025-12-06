"""
P站今日排行榜主界面
https://www.pixiv.net/ranking.php?mode=daily&content=illust
"""
# 内置库
import time
import json
import io
# 第三方库
import requests
from PIL import Image   # 图片格式转换(统一jpg)
from bs4 import BeautifulSoup

num_top_images = 10     # 抓取排行前几的图片
r18: bool = False      # 是否r18(必须加cookie)

url = f"https://www.pixiv.net/ranking.php?mode=daily{"_r18" if r18 else ""}&content=illust"     # 今日排行
# url = f"https://www.pixiv.net/ranking.php?mode=weekly{"_r18" if r18 else ""}&content=illust"    # 本周排行
# url = f"https://www.pixiv.net/ranking.php?mode=monthly{"_r18" if r18 else ""}&content=illust"   # 本月排行
# url = f"https://www.pixiv.net/ranking.php?mode=rookie&{"_r18" if r18 else ""}content=illust"    # 新人排行

headers = { # 不带cookie无法爬取r18的数据
    # "cookie": "",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net",
}
responds = requests.get(url=url,headers=headers,timeout=10)
print(f"P站排行界面响应状态:{responds.status_code}")
soup = BeautifulSoup(responds.text, "lxml") # 解析整个DOM
json = json.loads(soup.find("script", id="__NEXT_DATA__").text)
print(f"目前排行榜共有{len(json["props"]["pageProps"]["assign"]["contents"])}张图片")
# 遍历排行榜单的作品信息(内置id)
for index, artwork_info in enumerate(json["props"]["pageProps"]["assign"]["contents"]):
    # json响应，真正的url在里面
    json_respond = requests.get(
        url=f"https://www.pixiv.net/ajax/illust/{artwork_info["illust_id"]}?lang=zh",headers=headers,timeout=10)
    print(f"https://www.pixiv.net/ajax/illust/{artwork_info["illust_id"]}?lang=zh") # 藏着图片url的json地址
    # # 解析json数据拿到我真正想要的(图片url)
    # print(json_respond.json()["body"]["urls"]["original"])
    pic_url = json_respond.json()["body"]["urls"]["original"]
    # 判断链接是否有效(没有cookie的话r18链接无法获取)
    if pic_url:
        pic_respond = requests.get(url=pic_url, headers=headers, timeout=10)
    else:
        print(f"排行{index + 1}的插画获取失败")
        continue
    # 图片下载保存
    with Image.open(io.BytesIO(pic_respond.content)) as pic_file:   # 必须统一格式，有时候是png，大多为jpg
        pic_file.save(f"{time.time_ns()}.png", "PNG")   # 无损，但是图片大
    # 判断是否达到排行榜的位置
    if (index + 1) == num_top_images:
        break

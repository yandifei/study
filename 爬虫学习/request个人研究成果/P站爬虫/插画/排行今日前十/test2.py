"""
P站今日排行榜主界面
https://www.pixiv.net/ranking.php?mode=daily&content=illust
"""
# 内置库
import time
# 第三方库
import requests
from bs4 import BeautifulSoup

url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net"
}
responds = requests.get(url=url,headers=headers,timeout=10)
print(f"P站排行界面响应状态:{responds.status_code}")
print(responds.text)
# # 解析整个DOM
# soup = BeautifulSoup(responds.text, "lxml")
# # 图片导航标签
# picture_navigation_tags = soup.find_all("a", class_="relative group w-full")
# # 拿到源图链接
# for picture_navigation_tag in picture_navigation_tags:
#     print(picture_navigation_tag.strings)

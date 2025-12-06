"""
P站今日排行榜主界面

https://www.pixiv.net/ranking.php?mode=daily&content=illust
"""
import datetime
import re
import time

import requests
from asgiref.timeout import timeout

url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-encoding" : "gzip, deflate, br, zstd",    # 加了会乱码
    "accept-encoding" : "gzip, deflate, zstd",
    "accept-language" : "zh-CN,zh;q=0.9",
    "cache-control" : "max-age=0",
    # "cookie" : "",
    # "if-none-match" : "ivlzl36ukd2vyy",

    "priority" : "u=0, i",
    "sec-ch-ua" : '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    "sec-ch-ua-mobile" : "?0",
    "sec-ch-ua-platform" : '"Windows"',
    "sec-fetch-dest" : "document",
    "sec-fetch-mode" : "navigate",
    "sec-fetch-site" : "same-origin",
    "sec-fetch-user" : "?1",
    "upgrade-insecure-requests" : "1",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    # "referer": "https://www.pixiv.net"
}



download_pic_headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '',
    'priority': 'u=1, i',
    'purpose': 'prefetch',
    # 'referer': 'https://www.pixiv.net/artworks/138208295',
    'referer': 'https://www.pixiv.net',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    'x-middleware-prefetch': '1',
    'x-nextjs-data': '1',
}
# https://github.com/yandifei?submit=Search&q=dfsdfdsfsdfsdfsd&tab=stars&type=&sort=&direction=&submit=Search
responds = requests.get(
    url=url,
    headers=headers,
    timeout=10
)

# responds.encoding = "utf-8"
print(f"响应状态:{responds.status_code}")
# print(responds.text)


from bs4 import BeautifulSoup


soup = BeautifulSoup(responds.text, "lxml")
# 图片导航标签
picture_navigation_tags = soup.find_all("a", class_="relative group w-full")
# 拿到源图链接
for picture_navigation_tag in picture_navigation_tags:
    # print(picture_navigation_tag)
    # 源图片链接
    source_image_link = "https://www.pixiv.net" + picture_navigation_tag.get("href")
    print(source_image_link)
    source_image_link_responds = requests.get(
        url=url,
        headers=headers,
        timeout=10
    )
    print(source_image_link_responds.status_code)
    soup = BeautifulSoup(source_image_link_responds.text, "lxml")
    a_tags = soup.find_all("a", {"target": "_blank", "rel": "noopener", "style": "position: relative"})
    print(a_tags)

    # print(pic_responds.status_code)
    # with open(f"{time.time_ns()}.jpg", "wb") as pic:
    #     pic.write(pic_responds.content)

# <a href="https://i.pximg.net/img-original/img/2025/12/04/09/47/30/138208295_p0.jpg" class="sc-440d5b2c-3 jpNsVx gtm-expand-full-size-illust" target="_blank" rel="noopener" style="position: relative;"><img alt="#女の子 👻 - Noyu的插画" width="2486" height="3798" class="sc-440d5b2c-1 jnuqJZ" src="https://i.pximg.net/img-master/img/2025/12/04/09/47/30/138208295_p0_master1200.jpg" style="height: 983px;"><button class="buttonsOnArtworkPage btnOnThumb" data-xztitle="_图片查看器" style="display: flex; left: unset; right: -32px; top: 0px;" title="图片查看器">
#     <svg class="icon" aria-hidden="true">
#   <use xlink:href="#icon-zoom"></use>
# </svg></button><button class="buttonsOnArtworkPage btnOnThumb" data-xztitle="_复制图片和摘要" style="display: flex; left: unset; right: -32px; top: 40px;" title="复制图片和摘要">
#     <svg class="icon" aria-hidden="true">
#   <use xlink:href="#icon-copy"></use>
# </svg></button><button class="buttonsOnArtworkPage btnOnThumb" data-xztitle="_下载" style="display: flex; left: unset; right: -32px; top: 80px;" title="下载">
#     <svg class="icon" aria-hidden="true">
#   <use xlink:href="#icon-download"></use>
# </svg></button></a>
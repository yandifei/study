import datetime
import time

import requests


print(time.time_ns())

download_pic_headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '',
    'priority': 'u=1, i',
    'purpose': 'prefetch',
    'referer': 'https://www.pixiv.net',
    # 'referer': "",
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

pic_responds = requests.get(
        url="https://i.pximg.net/img-original/img/2025/12/04/00/06/08/138197616_p0.jpg",
        headers=download_pic_headers,
        timeout=10
    )
print(pic_responds.status_code)

with open(f"{time.time_ns()}.jpg", "wb") as pic:
    pic.write(pic_responds.content)


# headers = {
#     'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
# }
#
# pic_responds = requests.get(
#         url="https://www.pixiv.net/artworks/138208295",
#         headers=headers,
#         timeout=10
#
#     )
# print(pic_responds.status_code)
# with open("爬虫.html", "wb") as f:
#     f.write(pic_responds.content)
# print(pic_responds.text)
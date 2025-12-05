"""
P站今日排行榜主界面

https://www.pixiv.net/ranking.php?mode=daily&content=illust
"""
import requests

url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-encoding" : "gzip, deflate, br, zstd",    # 加了会乱码
    "accept-encoding" : "gzip, deflate, zstd",
    "accept-language" : "zh-CN,zh;q=0.9",
    "cache-control" : "max-age=0",
    # "cookie" : "",
    "if-none-match" : "ivlzl36ukd2vyy",

    "priority" : "u=0, i",
    "sec-ch-ua" : '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    "sec-ch-ua-mobile" : "?0",
    "sec-ch-ua-platform" : '"Windows"',
    "sec-fetch-dest" : "document",
    "sec-fetch-mode" : "navigate",
    "sec-fetch-site" : "same-origin",
    "sec-fetch-user" : "?1",
    "upgrade-insecure-requests" : "1",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

responds = requests.get(
    url=url,
    headers=headers
)

# responds.encoding = "utf-8"
print(f"响应状态:{responds.status_code}")
print(responds.text)


# from bs4 import BeautifulSoup
#
#
# soup = BeautifulSoup(responds.text, "lxml")
# h1 = soup.find("h1")
# print(h1.text)
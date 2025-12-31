
import requests

# num_top_images = 10     # 抓取排行前几的图片
mode = "daily"  # 排行模式（daily、weekly、monthly、rookie）
page = 1 # 第几页（1页50张画）
r18: bool = False      # 是否r18(必须加cookie)

# 每周、每日、每月、新人
url = f"https://www.pixiv.net/ranking.php?mode={mode}{"_r18" if r18 else ""}&content=illust&p={page}&format=json"

headers = { # 不带cookie无法爬取r18的数据
    # "cookie": "",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net",
}
responds = requests.get(url=url,headers=headers,timeout=10)
print(f"P站排行界面响应状态:{responds.status_code}")
# 遍历排行榜单的作品信息(内置id、url等)
for content in responds.json()["contents"]:
    # 拿到原图链接(原图有可能是png而不是jpg，所以这里是不稳定的)
    original_url: str = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace("_master1200", "")
    print(original_url)

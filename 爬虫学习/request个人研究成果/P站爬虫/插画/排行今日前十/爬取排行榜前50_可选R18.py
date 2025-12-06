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

num_top_images = 3     # 抓取排行前几的图片
r18: bool = True      # 是否r18(必须加cookie)

# url = f"https://www.pixiv.net/ranking.php?mode=daily{"_r18" if r18 else ""}&content=illust"     # 今日排行
url = f"https://www.pixiv.net/ranking.php?mode=weekly{"_r18" if r18 else ""}&content=illust"    # 本周排行
# url = f"https://www.pixiv.net/ranking.php?mode=monthly{"_r18" if r18 else ""}&content=illust"   # 本月排行
# url = f"https://www.pixiv.net/ranking.php?mode=rookie&{"_r18" if r18 else ""}content=illust"    # 新人排行

headers = { # 不带cookie无法爬取r18的数据
    "cookie": "first_visit_datetime_pc=2025-11-17%2018%3A37%3A19; p_ab_id=9; p_ab_id_2=6; p_ab_d_id=21178917; yuid_b=OZY2gAg; _ga=GA1.1.15955225.1763372242; _gcl_au=1.1.1695543687.1764916332; device_token=5e82edb2d13c39b7076d7bd783e21c44; c_type=25; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; PHPSESSID=106069815_4dqyRqeltTcqJiApWmfYFGTFVqg7nNrO; _ga_MZ1NL4PHH0=GS2.1.s1764916349$o2$g1$t1764916605$j16$l0$h0; _cfuvid=UA2hfTXdurrPgHCIgcRzkKVbiae5LUhh3ISHONwRIxE-1765005060148-0.0.1.1-604800000; cf_clearance=iTv9VFRsojictBVfKmP7a5fYqWDvAVWzzKqXg3qJVAM-1765042336-1.2.1.1-ucC5gWqOQjY0eXiK00bB_4NPP5A3gWOtsaGLlNClT1tAPJFK.u32YGe4c9H2CniTku.buzamFOqF.PJbQfJxEX_C8ou8nDiEuKPnTZNWNAwOAAfC4.tm_jdYh356XbEOsuoDPPFnyHQwEOrvctm_5JzpIEXFdC.qlNfvOw8p5GW_.CiTu1Jx6bS1b6UdxMw8MQAOwMF0Lt4bIxb8VQ8lgGBim929iZhtDV2AeK98hkU; _ga_75BBYNYN9J=GS2.1.s1765034425$o9$g1$t1765042338$j60$l0$h0; __cf_bm=smWKFqG_0C7x1uZ72ITJgNTlUY_ELPMOW8Oh9QQYGVM-1765042749-1.0.1.1-qYKwjrOjidxV.08vVobyDYtpiRg9rQVlwKKtHqWbqWZt8RzTXg47hNbo3AaKI7.1rnwsYKgwB_rtF6eqdPV2il061KdtYIgjTx97MOTe1H36lr27UIpTOTYzEQ05_0He",
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

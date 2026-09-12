
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


def get_real_url(illust_id: str) -> str:
    """
    获取图片真实url
    :param illust_id: 插画id
    :return: 图片真实url，不含错误
    """
    # 请求拿到所有不同分辨率及原图的url
    responds = requests.get(url=f"https://www.pixiv.net/ajax/illust/{illust_id}/pages", headers=headers, timeout=10)
    return responds.json()["body"][0]["urls"]["original"]



# 遍历排行榜单的作品信息(内置id、url等)
for index, content in enumerate(responds.json()["contents"]):
    # 拿到原图链接(原图有可能是png而不是jpg，所以这里是不稳定的)
    original_url: str = content["url"].replace("c/480x960/", "").replace("img-master", "img-original").replace("_master1200", "")
    # 图片请求
    responds = requests.get(url=original_url,headers=headers,timeout=10)
    # 判断图片是否404（可能是png图片格式的问题）
    if responds.status_code == 404:
        # 拿到真实有效稳定的url
        original_url = get_real_url(content["illust_id"])
        # 图片请求
        responds = requests.get(url=original_url,headers=headers,timeout=10)
    # 图片保存（榜单类型+排名）[页数-1即为过去，下标是0所以加1，乘50是过去的作品排名]
    with open(f"data/{mode}{(page - 1) * 50 + index + 1}.png", "wb") as pic_file:
        pic_file.write(responds.content)
    print(f"{mode}  {(page - 1) + index + 1}:{original_url}")
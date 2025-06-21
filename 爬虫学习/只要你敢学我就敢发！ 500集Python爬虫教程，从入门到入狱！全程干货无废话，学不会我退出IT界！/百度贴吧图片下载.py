import requests
from lxml import etree

"""
headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-encoding": "gzip, deflate, br, zstd",
    # "Accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    # "Cookie": '_TDID_CK=1750438984638; XFI=6f6e8eb0-4df8-11f0-ab04-a798bc7549b3; XFCS=6051C4E7CB2CFD11AC6DAF387C07C0A0F95D9B500B371EA62289412B3C8171F7; XFT=fAJv/xEE3xJ2mQ7WXbtJ8Qp7kRrWk1cYogeY2SU9uR8=; BAIDUID=6FE8C01CC758BCC9999541A318382737:FG=1; BAIDUID_BFESS=6FE8C01CC758BCC9999541A318382737:FG=1; __bid_n=196353a0c4e1152b6e0b66; BIDUPSID=6FE8C01CC758BCC9999541A318382737; PSTM=1744802376; H_WISE_SIDS=62325_62830_62968_63194_63243_63244_63248; H_PS_PSSID=60277_62325_62830_63147_63325_63402_63567_63563_63584_63577_63638_63627_63645_63646_63658_63673; BAIDU_WISE_UID=wapp_1750437726544_594; USER_JUMP=-1; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1750437727; HMACCOUNT=CE612411B421F2E9; arialoadData=false; ppfuid=undefined; video_bubble0=1; ZFY=:BV857LD8L8doA07QQNnVnfbNGNsIuPaJ4uIaPPKu1:Bk:C; XFI=8a60c790-4df5-11f0-94ee-b7a8f234fa82; _TDID_CK=1750437743425; 6333762c95037d16=oDjY6pOfkonWXCt%2BGV7M%2F4ZNLs5z%2FDpD3Qq2nWpA6XzQlMH5ISO1QJ6DEeR01Qfb0zF7dTN8i0bxVLSQnpsQ6HR1JGUmHZ5NWPpUjV3Sgp%2BGanAeqxIFfYgq47zuT5cJ60gGrCQrmSwBSq0LM9uXZKqVanFIubmNG9AWknJxABa5PviTMnt7Qzlbx5N8bpnUksqeD5GjCJt9H7Zu6OKEPFRNzj6FhjV0Ke%2B6kLL%2FtRi%2BMD%2FXOS466GGvVnAz1mW9FAztqVwDneNnt6QWnnwopbGHysg%2BsajnCt%2FAn4jehjlYOtxhEqaGJQ%3D%3D; XFCS=6FC2C0C7652D049B9C2CFA0592A3855BBAB313577D2CF37466874AD5C92027E7; XFT=14Xd7T7WQPQN1aNfPV9VJhcmNFwLbk606CPinYi2UN8=; wise_device=0; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1750438984; BA_HECTOR=2404a0ak010125012kaka5a0ah8ha01k5b52924; RT="z=1&dm=baidu.com&si=392cefd2-1431-46ef-a932-3b52db27816c&ss=mc51fd4e&sl=8&tt=c58&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&r=l9lqjau&ul=t645&hd=t64o"',
    # "Connection": "keep-alive",
    # "Host": "tieba.baidu.com",
    # "Sec-Ch-Ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    # "Sec-Ch-Ua-Mobile": "?0",
    # "Sec-Ch-Ua-Platform": '"Windows"',
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
}

proxies = {
    "https": "106.75.251.211:3128"
}

index_url = "https://tieba.baidu.com/p/5475267611"


# 只请求一次 + 错误处理
# try:
#     response = requests.get(index_url, headers=headers).text
    # response.raise_for_status()  # 自动检查4xx/5xx错误
    # print(response.status_code)
    # print(response.text)
# except requests.exceptions.RequestException as e:
#     print(f"请求失败: {e}")

# 没办法，确实拿不到数据，对面有返爬
response = requests.get(index_url, headers=headers).text
selector = etree.HTML(response)
image_urls = selector.xpath('//img[@class="BDE_Image"]/@src')

offset = 0  # 用来命名图片名字
# 遍历图片的url
for image_urls in image_urls:
    print(image_urls)
    # 获得单个图片url的二进制内容
    image_content = requests.get(image_urls).content

    # 打开文件
    with open("{}.jpg".format(offset), "wb") as f:
        f.write(image_content)  # 写入二进制数据

"""
url = "https://movie.douban.com/top250"   # 我换一个豆瓣250爬吧，用来学习，百度贴吧返爬技术太叼了
# 定义请求头伪装自己
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
}

response = requests.get(url, headers=headers)
# 打印状态码
print(response.status_code)

# 打印内容
print(response.text)


response = response.content.decode()
# 创建查询解析器对象
selector = etree.HTML(response)
# 查询所有img的标签，img标签条件是width="100" ，拿到所有有符合该条件的标签，仅提取src的url
image_urls = selector.xpath('//img[@width="100"]/@src')
print(image_urls, len(image_urls))
# 这个是拿到图片的电影名字
image_names = selector.xpath('//img[@width="100"]/@alt')
print(image_names, len(image_names))

# 解析图片的url和电影名称(用来做图片名称)
for img_url, image_name in zip(image_urls, image_names):
    # 发起get请求拿到图片的二进制数据
    response = requests.get(img_url, headers=headers)
    # 创建文件并写入数据
    with open(f"./百度贴吧爬虫图片/{image_name}.webp", "wb") as img:
        img.write(response.content)   # 把请求图片的得到的二进制数据写入进入文件里面去
    print(img_url, image_name)
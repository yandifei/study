# 内置库
import random
import re
# 第三方库
import requests
# 搜索关键词
theme = "白丝"



headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
        }

def get(url):
    return requests.get(url,
                     headers=headers,
                     timeout=10)
response = get(fr"https://www.yeitu.com/index.php?m=sch&c=index&a=init&typeid=&siteid=1&q={theme}")
# print(response.text)
# 检查是否有用搜索结果
search_result = re.findall(r'<ul class="list_box">\n {8}未找到搜索结果</ul>', response.text)
# 没有搜索结果
if search_result:
    print(f"这个关键词`{theme}`没有找到相关图片结果")
    exit()  # 退出操作
# 拿到所有搜索结果的链接
all_search_link = re.findall(r'<h5><a href="(.*?)" target="_blank">', response.text)
# 选取其中的一个随机链接
link = random.choice(all_search_link)
print(link)
response = get(fr"{link}")

# 最大图片数
max_pic_num = re.search(r'\.\.<a.*?>(?P<page_num>\d+)</a>', response.text).group("page_num")

# all_pic_link
# print()
# 下载的图片数量
for i in range(int(max_pic_num)):
    # 拼接需要爬取图片的源网址
    source_page_url = link + f"_{i}"
    response = get(fr"{source_page_url}")
    # 图片地址
    pic_url = re.search(fr'<a href="{source_page_url}"><img alt=".*?" src="(.*?)"></a>', response.text).group(0)
    # 请求链接返回图片
    response = get(fr"{source_page_url}")
    # 保存请求的图片
    with open(f"logs/下载缓存/爬虫图片.png", 'wb') as f:
        # 使用 response.iter_content 逐块写入，特别是处理大文件时，可以节省内存
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # 确保块不为空
                f.write(chunk)




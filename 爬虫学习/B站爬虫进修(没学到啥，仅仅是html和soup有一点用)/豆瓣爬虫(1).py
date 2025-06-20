import requests
from bs4 import BeautifulSoup

# 请求头伪装
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}

# 翻页操作，这里实际上就只是修改url的调整索引
for start_num in range(0, 250, 25):
    # 打印当前页
    # print(start_num)

    response = requests.get(f"https://movie.douban.com/top250?start={start_num}", headers=header)
    # 打印状态码
    # print(response.status_code)
    # 打印html信息
    # print(response.text)

    # 拿到html文本
    html = response.text
    # 给BeautifulSoup解析html
    soup = BeautifulSoup(html, "html.parser")
    # 找到所有span标签后找找到符合class为title的标签
    all_titles = soup.find_all("span", attrs={"class": "title"})
    # for解析
    for title in all_titles:
        title_string = title.string # string是只拿到它的文本，去掉html的标签
        if "/" not in title_string:
            print(title_string)
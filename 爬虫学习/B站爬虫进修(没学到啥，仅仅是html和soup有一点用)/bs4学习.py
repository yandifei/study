import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
content = requests.get(url).text
# print(content)
soup = BeautifulSoup(content, "html.parser")
# 打印html第一个p元素
print(soup.p)
# 打印html的第一个img元素
print(soup.img)

# 使用findAll
all_prices = soup.findAll("p", attrs={"class": "price_color"})  # 找p标签的html
# for遍历price_color的p标签
for price in all_prices:
    print(price.string[2:])


# 找到书名
all_titles = soup.findAll("h3")
for title in all_titles:
    all_links = title.findAll("a")
    for link in all_links:
        print(link.string)
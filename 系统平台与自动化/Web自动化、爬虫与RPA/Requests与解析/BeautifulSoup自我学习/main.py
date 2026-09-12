"""
解析器	使用方法	优势	劣势
Python标准库	BeautifulSoup(markup, "html.parser")	Python内置，执行较快	速度不及lxml
lxml HTML解析器	BeautifulSoup(markup, "lxml")	速度快，容错强	需要C依赖
lxml XML解析器	BeautifulSoup(markup, "xml")	唯一支持XML的解析器	需要C依赖
html5lib	BeautifulSoup(markup, "html5lib")	最好的容错性，浏览器方式解析	速度慢
"""

from bs4 import BeautifulSoup

# 基本用法

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time...</p>
</body></html>
"""

soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())  # 格式化输出

# 获取标题
print(type(soup.title))
print(type(soup.title.string))

print(soup.title)
print(soup.title.string)


# 获取所有链接
for link in soup.find_all('a'):
    print(link.get('href'))

# 获取所有文本
print(soup.get_text())


"""
四、对象类型
"""
# 1. Tag对象
# 与XML/HTML原生tag相同
tag = soup.b
tag.name  # 'b'
tag['class']  # 获取属性
tag.attrs  # 获取所有属性

# 2. NavigableString对象
# 包装tag中的文本内容
tag.string  # 'Extremely bold'
type(tag.string)  # <class 'bs4.element.NavigableString'>

# 3. BeautifulSoup对象
# 表示整个文档
soup.name  # '[document]'

# 4. 特殊对象
# Comment：注释
# Stylesheet：CSS样式
# Script：JavaScript代码
# Template：HTML模板


# 五、遍历文档树
# 子节点
soup.head  # 获取head标签
soup.head.contents  # 子节点列表
soup.head.children  # 子节点迭代器
soup.head.descendants  # 所有子孙节点
# 父节点
title_tag.parent  # 父节点
link.parents  # 所有父辈节点
# 兄弟节点
tag.next_sibling  # 下一个兄弟节点
tag.previous_sibling  # 上一个兄弟节点
tag.next_siblings  # 后面所有兄弟节点
tag.previous_siblings  # 前面所有兄弟节点
# 前后节点
tag.next_element  # 下一个解析对象
tag.previous_element  # 上一个解析对象
tag.next_elements  # 后面所有解析对象
tag.previous_elements  # 前面所有解析对象
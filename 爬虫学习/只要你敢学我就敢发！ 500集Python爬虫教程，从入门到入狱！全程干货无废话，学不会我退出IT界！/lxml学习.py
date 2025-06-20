from lxml import etree
import requests

text = requests.get("https://baidu.com").content.decode()


html = etree.HTML(text)
print(etree.tostring(html))

result = html.xpath("//li/@class")

result2 = html.xpath("/html/a") # /html是目录形式(/root/home一样的绝对路径)

print(result)


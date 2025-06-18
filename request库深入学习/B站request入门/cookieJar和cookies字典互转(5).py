import requests

url = "http://www.baidu.com"

response = requests.get(url)

# 省流：cookie有两种形式，分别是dict类型和RequestsCookieJar类型；utils模块提供了双向转换函数
# 字符串形式打印cookie
print(response.cookies)

# 把cookiejar转为cookies字典
dict_cookies = requests.utils.dict_from_cookiejar(response.cookies)
print(dict_cookies)

# 把cookies字典转为cookiejar
jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
print(jar_cookies)

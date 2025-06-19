"""
利用requests.session进行状态保持
requests模块中的Session类能够自动处理发送请求获取响应过程中产生的cookie，进而
达到状态保持的目的。接下来我们就来学习它

requests.session的作用以及应用场景
requests.session的作用
自动处理cookie，即下一次请求会带上前一次的cookie
requests.session的应用场景
自动处理连续的多次请求过程中产生的cookie
"""
import requests

url = "https://baidu.com"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"

}
session = requests.session()
response = session.get(url, headers)
response = session.post(url, data)
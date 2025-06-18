"""
代理分类
    正向代理：
        VPN(虚拟专用网络)
        用客户端发送请求给代理，代理转发请求。
        1. 高匿代理(Elite proxy或High Anonymity Proxy):
        高匿代理让别人根本无法发现你是在用代理，所以是最好的选择。毫无疑问使用高匿代理效果最好。
        请求头
        REMOTE_ADDR = Proxy IP
        HTTP_VIA = not determined
        HTTP_X_FORWARDED_FOR = not determined
        2. 匿名代理(Anonymous Proxy):
        使用匿名代理，别人只能知道你用了代理，无法知道你是谁。
        REMOTE_ADDR = Proxy IP
        HTTP_VIA = Proxy IP
        HTTP_X_FORWARDED_FOR = Proxy IP
        3. 透明代理(Transparent Proxy):
        透明代理虽然可以直接“隐藏"你的IP地址，但是还是可以查到你是谁。
        请求头
        REMOTE_ADDR = Proxy IP
        HTTP_VIA = Proxy IP
        HTTP_X_FORWARDED_FOR = Your IP
    反向代理：
        服务器把消息转化给客户端，防DDoS攻击，也能实现分流，避免拥堵
"""
import requests

url = "http://www.baidu.com"

# 未使用代理的情况
response = requests.get(url)
print(response.text)

# 使用代理的情况（自己没有构建请求头的时候，代理可能会构建请求头的信息发给服务器）
# 使用代理失败有2种情况：1.卡顿 2. 报错
# 支持https极大可能支持http，但是支持http的一般不支持https
# 学习的网址：https://www.kuaidaili.com/free/intr
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
#
# }
proxies = {
    "https" : "http://8.219.97.248:80"   # 上海的
    # "https" : "http://218.95.81.51:9000",
}
proxies_response = requests.get(url, proxies=proxies)
print(proxies_response.text)

"""
User-Agent: 客户端标识(浏览器类型/版本等)
Accept: 客户端能够接收的内容类型
Accept-Language: 客户端偏好的语言'zh-CN',
Accept-Encoding: 客户端支持的压缩编码
Referer: 当前请求的来源页面URL
Cookie: 发送给服务器的cookie数据
Authorization: 认证信息(如Bearer token)
Content-Type: 请求体的MIME类型(用于POST/PUT请求)
"""
import requests
url = "http://www.baidu.com"
# url = "https://t.alcy.cc/moe"


response = requests.get(url)

# 打印响应的大小
print(len(response.content.decode()))  # 拿到返回的字节(二进制)数量
print(response.content.decode())    # 打印解码后的二进制数据


# 自己构建请求头
# 1. User-Agent: 客户端标识(浏览器类型/版本等)，默认是python，1秒被抓
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"

}

# 发送带请求头的请求
responds1 = requests.get(url,headers=headers)
# 打印带请求头响应的大小（这回带上自定会的请求头了）
print(len(responds1.content.decode()))  # 拿到返回的字节(二进制)数量
print(responds1.content.decode())    # 打印解码后的二进制数据
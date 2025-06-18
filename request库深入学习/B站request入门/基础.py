import requests

url = "http://www.baidu.com"
# url = "https://t.alcy.cc/moe"
r = requests.get(url)
"""X
# 手动设置编码格式
r.encoding = "utf-8"
print(r.encoding)

# 打印源码str类型的数据
print(r.text)

# 存储bytes类型的响应源码,可以进行decode操作
print(r.content)

# decode就是把bytes类型的源码通过encoding解码
print(r.content.decode())   # bytes.decode() 方法的默认编码是 utf-8
# r.content.decode()   # 等价于 r.content.decode(encoding='utf-8')

# 响应对象的其它常用属性或方法
# 响应url
print(r.url)

# 状态码
print(r.status_code)

# 响应对应的请求头(请求头)
print(r.request.headers)
# User-Agent: 客户端标识(浏览器类型/版本等)
# Accept: 客户端能够接收的内容类型
# Accept-Language: 客户端偏好的语言'zh-CN',
# Accept-Encoding: 客户端支持的压缩编码
# Referer: 当前请求的来源页面URL
# Cookie: 发送给服务器的cookie数据
# Authorization: 认证信息(如Bearer token)
# Content-Type: 请求体的MIME类型(用于POST/PUT请求)

# 响应头
print(r.headers)
# Server: 服务器软件信息
# Content-Type: 响应体的MIME类型
# Content-Length: 响应体的大小(字节)
# Content-Encoding: 响应体使用的编码压缩方式
# Cache-Control: 缓存控制指令
# Set-Cookie: 服务器设置的cookie
# Location: 重定向目标URL(用于3xx响应)
# Expires: 响应过期时间
# Last-Modified: 资源最后修改时间

# 打印响应设置cookies
print(r.cookies)

# 打印响应的大小
print(len(r.content.decode()))  # 拿到返回的字节(二进制)数量
"""












# with open("./image.jpg", 'wb') as file:
#     # 分块写入文件，适合大文件下载
#     for chunk in r.iter_content():
#         file.write(chunk)


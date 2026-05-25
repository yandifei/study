"""测试的url
# GET 请求
http://127.0.0.1:21325/status
http://127.0.0.1:21325/docs
http://127.0.0.1:21325/openapi.json
http://127.0.0.1:21325/ask/你好
http://127.0.0.1:21325/answer
http://127.0.0.1:21325/conversations/title/list
http://127.0.0.1:21325/conversations/count

# POST 请求
http://127.0.0.1:21325/conversations  # 创建新会话
http://127.0.0.1:21325/ask  # 提问（带JSON body）

# DELETE 请求
http://127.0.0.1:21325/conversations  # 删除第一个会话
http://127.0.0.1:21325/conversations/新对话  # 删除指定会话（根据JSON）

# PUT 请求
http://127.0.0.1:21325/conversations  # 切换会话
http://127.0.0.1:21325/conversations/关于 API  # 通过标题切换会话
"""

import requests

url = "http://127.0.0.1:21325/ask"
# 文本对话模式
json_data1 = {
    "question": "你好，介绍一下你自己",
}

# 图形对话模式
json_data2 = {
    "question": "给我生成类似的图片",
    "files": "data/test.png"
}

response = requests.post(url, json=json_data2)
print(response.json())

"""其他语言、方式请求接口
cmd：
# 1. 获取状态
curl -X GET "http://127.0.0.1:21325/status"

# 2. 创建新会话
curl -X POST "http://127.0.0.1:21325/conversations"

# 3. 切换会话
curl -X PUT "http://127.0.0.1:21325/conversations"
# 或通过标题切换
curl -X PUT "http://127.0.0.1:21325/conversations/关于%20API"

# 4. 删除第一个会话
curl -X DELETE "http://127.0.0.1:21325/conversations"
# 删除指定会话（注意URL编码）
curl -X DELETE "http://127.0.0.1:21325/conversations/新对话"

# 5. 提问（带文件）
curl -X POST "http://127.0.0.1:21325/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"识别验证码图片仅返回数字\", \"files\": \"data/验证码1.jpg\"}"

# 6. 固定问题
curl -X GET "http://127.0.0.1:21325/ask/你好"

# 7. 获取回答
curl -X GET "http://127.0.0.1:21325/answer"

# 8. 获取会话列表
curl -X GET "http://127.0.0.1:21325/conversations/title/list"

# 9. 获取会话总数
curl -X GET "http://127.0.0.1:21325/conversations/count"

# 10. 获取文档
curl -X GET "http://127.0.0.1:21325/docs"
curl -X GET "http://127.0.0.1:21325/openapi.json"


PowerShell
curl -X POST http://127.0.0.1:21325/ask `
     -H "Content-Type: application/json" `
     -d '{"question": "联网搜索今天的国际大事"}'
"""

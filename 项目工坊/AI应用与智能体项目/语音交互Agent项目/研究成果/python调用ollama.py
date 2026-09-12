import re

# from ollama import chat
# from ollama import ChatResponse
#
# response: ChatResponse = chat(model='qwen3:8b', messages=[
#   {
#     'role': 'user',
#     'content': '你好',
#   },
# ])
# print(response['message']['content'])
# # 或直接从响应对象访问字段
# print(response.message.content)

# """分割思考内容和回复文本"""
# response_text = response['message']['content']
# thinking_content = re.search(r'<think>(.*?)</think>', response_text, re.DOTALL)
# final_message = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL).strip()
# if thinking_content:
#     print("思考过程:", thinking_content.group(1))
# print("最终回复:", final_message)

# 流式响应
from ollama import chat

stream = chat(
    model="gemma3",
    messages=[{'role': 'user', 'content': "你好"}],
    stream=True,
)
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

# """分割思考内容和回复文本"""
# think_text =  ""
# for chunk in stream:
#     # 如果没有出现</think>就收录内容
#     if (text := chunk['message']['content']) != "</think>":
#         think_text += text
#     # 结束思考
#     else:
#         # 去掉流式的开头<think>
#         think_text = think_text.removeprefix("<think>\n")
#         # 打印思考内容
#         print(think_text)
#         # 退出遍历
#         break
# # 遍历非思考内容
# else:
#     for chunk in stream:
#         print(chunk['message']['content'], end='', flush=True)

"""
自定义客户端
可以通过实例化Client或AsyncClient从创建自定义客户端ollama。

所有额外的关键字参数都被传递到httpx.Client.

from ollama import Client
client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='gemma3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
"""


"""
异步客户端
该类AsyncClient用于发起异步请求。可以配置与该类相同的字段Client

import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  async for part in await AsyncClient().chat(model='gemma3', messages=[message], stream=True):
    print(part['message']['content'], end='', flush=True)

asyncio.run(chat())
"""
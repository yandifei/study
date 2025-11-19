from google import genai
from google.genai import types

# 客户端从环境变量“ gemini_api_key”获取API键。
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="介绍一下你自己，你是什么模型",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # 禁止思考(减少token和增加速度)
    ),

)
print(response.text)
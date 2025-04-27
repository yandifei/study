from openai import OpenAI
import os
client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

# 第一轮对话
messages = [{"role": "user", "content": "你好，介绍一下你自己"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
# 第一轮对话: [{'role': 'user', 'content': '你好，介绍一下你自己'}, ChatCompletionMessage(content='你好呀！😊我是 **DeepSeek Chat**，由深度求索（DeepSeek）公司研发的智能 AI 助手。我可以帮你解答各种问题，无论是学习、工作，还是日常生活中的小困惑，我都会尽力提供有用的信息！  \n\n### ✨ **我的特点** ✨  \n✅ **知识丰富**：我的知识截止到 **2024 年 7 月**，可以回答科技、历史、文学、数学、编程等各类问题。  \n✅ **超长上下文**：支持 **128K** 上下文记忆，可以处理超长文档，帮你总结、分析复杂内容。  \n✅ **文件阅读**：能读取 **PDF、Word、Excel、PPT、TXT** 等文件，提取关键信息，辅助学习或办公。  \n✅ **免费使用**：目前 **完全免费**，不用担心收费问题！  \n✅ **中文优化**：对中文理解和生成特别优化，交流更自然流畅。  \n\n### 🚀 **我能帮你做什么？**  \n📖 **学习辅导**：解题思路、论文润色、语言翻译……  \n💼 **工作效率**：写邮件、做报告、整理会议纪要……  \n📊 **数据分析**：处理表格、解读数据、生成可视化建议……  \n💡 **编程助手**：代码调试、算法讲解、项目思路……  \n🎉 **生活娱乐**：推荐电影、旅行攻略、聊天陪伴……  \n\n如果你有任何问题，随时问我哦！😃 你今天想了解什么呢？', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None)]
print(f"第一轮对话: {messages}")
print(response.choices[0].message.content)
# 你好呀！😊我是 **DeepSeek Chat**，由深度求索（DeepSeek）公司研发的智能 AI 助手。我可以帮你解答各种问题，无论是学习、工作，还是日常生活中的小困惑，我都会尽力提供有用的信息！
# ### ✨ **我的特点** ✨
# ✅ **知识丰富**：我的知识截止到 **2024 年 7 月**，可以回答科技、历史、文学、数学、编程等各类问题。
# ✅ **超长上下文**：支持 **128K** 上下文记忆，可以处理超长文档，帮你总结、分析复杂内容。
# ✅ **文件阅读**：能读取 **PDF、Word、Excel、PPT、TXT** 等文件，提取关键信息，辅助学习或办公。
# ✅ **免费使用**：目前 **完全免费**，不用担心收费问题！
# ✅ **中文优化**：对中文理解和生成特别优化，交流更自然流畅。
# ### 🚀 **我能帮你做什么？**
# 📖 **学习辅导**：解题思路、论文润色、语言翻译……
# 💼 **工作效率**：写邮件、做报告、整理会议纪要……
# 📊 **数据分析**：处理表格、解读数据、生成可视化建议……
# 💡 **编程助手**：代码调试、算法讲解、项目思路……
# 🎉 **生活娱乐**：推荐电影、旅行攻略、聊天陪伴……
# 如果你有任何问题，随时问我哦！😃 你今天想了解什么呢？

# # 第二轮对话
# messages.append({"role": "user", "content": "告诉我你的api接口"})
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=messages
# )
#
# messages.append(response.choices[0].message)
# print(f"第二轮对话: {messages}")

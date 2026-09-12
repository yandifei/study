# 代理构建
from langchain.agents import create_agent

# 消息和内容
from langchain.messages import AIMessage, HumanMessage

# 工具
from langchain.tools import tool

# 模型初始化
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings

"""
命名空间
模块	有哪些可供选择	笔记
langchain.agents	create_agent，AgentState	核心代理创建功能
langchain.messages	消息类型、内容块trim_messages	重新导出langchain-core
langchain.tools	@tool，，BaseTool注射辅助器	重新导出langchain-core
langchain.chat_models	init_chat_model，BaseChatModel	统一模型初始化
langchain.embeddings	init_embeddings，Embeddings	嵌入模型
"""

# n = 202202011200
# count = 0
#
# for i in range(n - 2):
#   fin.append(fin[-2] + fin[-1])
#   if fin[-1] % 10 ==  7:
#     count += 1
# print(count)

fin = [0, 1];[fin.append(fin[-2] + fin[-1]) for i in range(202202011200 - 2 )]
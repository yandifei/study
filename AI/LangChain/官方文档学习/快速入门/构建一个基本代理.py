from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """获取给定城市的天气。"""
    return f"{city}今天是阳光!"

agent = create_agent(
    model="deepseek-chat",
    tools=[get_weather],
    system_prompt="你是一个得力的助手",
)

# 运行代理
agent.invoke(
    {"messages": [{"role": "user", "content": "广州的天气怎么样"}]}
)

# 输出信息(非官方)
# respond = agent.invoke(
#     {"messages": [{"role": "user", "content": "广州的天气怎么样"}]}
# )
# print(respond.values())
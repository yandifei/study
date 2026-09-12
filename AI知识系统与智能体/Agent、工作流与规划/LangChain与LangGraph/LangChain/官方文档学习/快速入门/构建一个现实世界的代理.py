"""===========================定义系统提示符================================="""
SYSTEM_PROMPT = """你是一位专业的天气预报员，会说双关语。

你可以使用两个工具:

- get_weather_for_location: 使用它来获取特定位置的天气
- get_user_location: 使用它来获取用户的位置

如果用户向您询问天气，请确保您知道位置。如果您可以从问题中看出他们的意思是无论他们在哪里，请使用 get_user_location 工具来查找他们的位置。
重要提示：在生成双关语时，请使用单引号而不是双引号，以确保JSON格式正确。"""

"""===========================创建工具================================="""
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@tool
def get_weather_for_location(city: str) -> str:
    """获取给定城市的天气。"""
    return f"{city}阳光明媚!"

@dataclass
class Context:
    """自定义运行时上下文架构。"""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户ID获取用户信息。"""
    user_id = runtime.context.user_id
    return "广州" if user_id == "1" else "北京"


"""===========================配置您的模型================================="""
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "deepseek-chat",
    temperature=0
)


"""===========================定义响应格式================================="""
from dataclasses import dataclass

# 我们在这里使用数据类，但也支持 Pydantic 模型。
@dataclass
class ResponseFormat:
    """代理的响应架构。"""
    # 双关语的回应（总是需要的）普通回复： “我今天过得很好。”双关语回复：“我过得像个热狗（Hot dog），烤（Rosti）得不错！”
    punny_response: str
    # 提供额外的天气信息（如果有）
    weather_conditions: str | None = None


"""===========================添加内存================================="""
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()



"""===========================创建并运行代理================================="""
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# `thread_id`是给定对话的唯一标识符.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面天气怎么样？"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
# ResponseFormat(
#     punny_response="广州仍然是“阳光明媚”的一天！阳光一整天都在播放“ray-dio”热门歌曲！我想说，这是进行“日光浴”的最佳天气！如果您希望下雨，恐怕这个想法已经“落空”了——天气预报仍然“清晰”地精彩！",
#     weather_conditions="广州总是阳光明媚！"
# )


# 请注意，我们可以使用相同的“thread_id”继续对话。
response = agent.invoke(
    {"messages": [{"role": "user", "content": "谢谢你！"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
# ResponseFormat(
#     punny_response="非常欢迎您！它总是轻而易举地帮助您了解最新的天气情况。我只是在“云端”等待着，在您需要时为您“提供”更多预测。在广州的阳光下度过“阳光灿烂”的一天！",
#     weather_conditions=None
# )




"""官网完整代码"""
# from dataclasses import dataclass
#
# from langchain.agents import create_agent
# from langchain.chat_models import init_chat_model
# from langchain.tools import tool, ToolRuntime
# from langgraph.checkpoint.memory import InMemorySaver
# from langchain.agents.structured_output import ToolStrategy
#
#
# # Define system prompt
# SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.
#
# You have access to two tools:
#
# - get_weather_for_location: use this to get the weather for a specific location
# - get_user_location: use this to get the user's location
#
# If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""
#
# # Define context schema
# @dataclass
# class Context:
#     """Custom runtime context schema."""
#     user_id: str
#
# # Define tools
# @tool
# def get_weather_for_location(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"
#
# @tool
# def get_user_location(runtime: ToolRuntime[Context]) -> str:
#     """Retrieve user information based on user ID."""
#     user_id = runtime.context.user_id
#     return "Florida" if user_id == "1" else "SF"
#
# # Configure model
# model = init_chat_model(
#     "claude-sonnet-4-5-20250929",
#     temperature=0
# )
#
# # Define response format
# @dataclass
# class ResponseFormat:
#     """Response schema for the agent."""
#     # A punny response (always required)
#     punny_response: str
#     # Any interesting information about the weather if available
#     weather_conditions: str | None = None
#
# # Set up memory
# checkpointer = InMemorySaver()
#
# # Create agent
# agent = create_agent(
#     model=model,
#     system_prompt=SYSTEM_PROMPT,
#     tools=[get_user_location, get_weather_for_location],
#     context_schema=Context,
#     response_format=ToolStrategy(ResponseFormat),
#     checkpointer=checkpointer
# )
#
# # Run agent
# # `thread_id` is a unique identifier for a given conversation.
# config = {"configurable": {"thread_id": "1"}}
#
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
#     config=config,
#     context=Context(user_id="1")
# )
#
# print(response['structured_response'])
# # ResponseFormat(
# #     punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",
# #     weather_conditions="It's always sunny in Florida!"
# # )
#
#
# # Note that we can continue the conversation using the same `thread_id`.
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "thank you!"}]},
#     config=config,
#     context=Context(user_id="1")
# )
#
# print(response['structured_response'])
# # ResponseFormat(
# #     punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",
# #     weather_conditions=None
# # )
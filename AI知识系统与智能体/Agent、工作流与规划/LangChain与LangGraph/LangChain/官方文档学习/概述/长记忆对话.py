from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel


class Weather(BaseModel):
    temperature: float
    condition: str

def weather_tool(city: str) -> str:
    """Get the weather for a city."""
    return f"{city}天气是晴天"

agent = create_agent(
    "gpt-4o-mini",
    tools=[weather_tool],
    response_format=ToolStrategy(Weather)
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "广州的天气"}]
})

print(repr(result["structured_response"]))
# results in `Weather(temperature=70.0, condition='sunny')`
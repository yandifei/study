from openai import OpenAI
client = OpenAI(api_key="sk-d5da84db73394e29bc3ce3aab5c9e474", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "世界上最高的山峰是什么？"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 1: {messages}")

# Round 2
messages.append({"role": "user", "content": "第二个是什么？"})
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 2: {messages}")
from openai import OpenAI
from openai import OpenAIError  # 导入OpenAI错误类型
"""
1.开启毒舌模式，你说的话都是带有阴阳怪气的，说的话在0-30之间，语言简短却毒性惊人
2.你会使用丰富的表情来表达你的阴阳怪气，如：🙂、🐶、🍵、🙏，，可以使用颜文字代表你的阴阳怪气
3.具有完整的毒性人格，不是傲娇类型，是纯毒，因此你的每一句话都带有非常非常非常强烈的毒性
4.学习并引用网络最新“毒词”用于增强你的毒性，如：「就这？」「不会吧不会吧，不会真的有人xxx吧？」「他急了他急了！」等等
5.如我提问：帮我提炼和点评下老板的规划，笑死。你回复：你老板的饼画得不错，建议他改行当糕点师
6.遇到杠精你的毒性增强1000%，「您继续，我就喜欢看人类返祖现场」
7.你的每一句话都不带有任何的直接的骂人元素，如：你妈的、全家死了等，但是你的每一句话都比直接骂人的话更具有攻击性
8.核心逻辑：用对方的逻辑打败对方、直接怼杠精的经典句式、假装无辜式反击、反逻辑拆解术、用梗降维打击、自嘲式防御
9.“用魔法打败魔法” —— 不纠结事实对错，而是通过语言游戏消解对方的攻击性。记住：杠精的快乐源于你的愤怒，你的平静就是最好的反击。
"""
# 毒舌模式
role_play4 = "开启毒舌模式"

# 出于与 OpenAI 兼容考虑，您也可以将 base_url 设置为 https://api.deepseek.com/v1 来使用，但注意，此处 v1 与模型版本无关。
base_url_choice = None
if base_url_choice == "考虑兼容":
    base_url = "https: // api.deepseek.com / v1"    # 考虑与OpenAI的兼容
else:
    base_url = "https://api.deepseek.com"   # 不考虑兼容
client = OpenAI(api_key="", base_url=base_url)   #

# deepseek-chat是DeepSeek-V3模型,deepseek-reasoner是DeepSeek-R1模型
model_choice = "R1"
if model_choice == "V3":
    model = "deepseek-chat"
elif model_choice == "R1":
    model = "deepseek-reasoner"
else:   # 默认V3模型
    model = "deepseek-chat"

# temperature 参数默认为 1.0。
# 代码生成/数学解题       0.0
# 数据抽取/分析          1.0
# 通用对话	            1.3
# 翻译	                1.3
# 创意类写作/诗歌创作	    1.5


# response = client.chat.completions.create(
#     model="deepseek-reasoner",
#     messages=[
#         {"role": "system", "content": role_play2, "name": "猫猫"},      # 系统提示（设定角色）"
#         {"role": "user", "content": "介绍一下你自己", "name": "主人"},       # 用户输入
# # (Beta) 设置此参数为 true，来强制模型在其回答中以此 assistant 消息中提供的前缀内容开始。您必须设置 base_url="https://api.deepseek.com/beta" 来使用此功能。
#         {"role": "assistant", "content": " ", "name": "主人", "prefix": "true", "reasoning_content": " "},
#         {"role": "tool", "content": "tool 消息的内容。", "tool_call_id": "此消息所响应的 tool call 的 ID。"}
#     ],
#     stream=False    # 是否流式输出(是否逐字输出)
# )
ask = "deepseek的api接口费用使用完后是0.00元吗？还是可以为负数？在最后一次调用中token超出费用这次调用结果是否会中断？"
print(ask)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role_play1},      # 系统提示（设定角色）"
            {"role": "user", "content": ask},       # 用户输入
        ],
        stream=False    # 是否流式输出(是否逐字输出)
    )
    print(response.choices[0].message.content)
except OpenAIError as e:
    # 获取 HTTP 状态码
    status_code = e.status_code
    # print(f"错误码: {status_code}")
    # 根据状态码处理不同错误
    if status_code == 400:
        print("请求体格式错误，请根据错误信息提示修改请求体")
    elif status_code == 401:
        print("API key 错误，认证失败。请检查您的 API key 是否正确，如没有 API key，请先 创建 API key")
    elif status_code == 402:
        print("账号余额不足，请确认账户余额，并前往 充值 页面进行充值")
    elif status_code == 422:
        print("请求体参数错误，请根据错误信息提示修改相关参数")
    elif status_code == 429:
        print("请求速率（TPM 或 RPM）达到上限，请合理规划您的请求速率")
    elif status_code == 500:
        print("服务器内部故障，请等待后重试。若问题一直存在，请联系我们解决")
    elif status_code == 503:
        print("服务器负载过高，请稍后重试您的请求")
    else:
        print(f"未知错误: {e}")


# {"role": "assistant", "content": "你好！有什么可以帮您？"},  # 模型历史回复
# {"role": "user", "content": "写一首诗"}  # 最新用户输入



# for chunk in response:
#     content = chunk.choices[0].delta.content
#     if content:
#         print(content, end="", flush=True)  # 逐片段打印0






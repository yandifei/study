# <center>DeepseekConversationEngine(deepseek对话引擎)</center>
**对应的是deepseek_conversation_engine.py这个文件中的DeepseekConversationEngine类**
目标是最大化利用deepseek的api，面对不同场景使用不同的模型，给定不同的策略。以提供对话策略为主但又添加api余额查询、token数精准计算等实用的功能。
[DeepSeek API官方文档](https://api-docs.deepseek.com/zh-cn/):https://api-docs.deepseek.com/zh-cn/
## 核心能力：
- 密钥安全读取和校验
- 多模式对话管理（V3/R1）
- 温度参数动态调节
- Token消耗精准计算
- API资源监控预警
  
## 接口兼容选择
在DeepseekConversationEngine这个类中有client这个属性
```python
self.client = OpenAI(api_key=self.__DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
```
官方声明：出于与 OpenAI 兼容考虑可以将 base_url 设置为 https://api.deepseek.com/v1 来使用，但注意，此处 v1 与模型版本无关。
建议：
优先兼容模式：如果你需要复用现有 OpenAI 代码或第三方工具。
使用原生路径：如果需要体验 DeepSeek 独有的功能或参数（如果有），需参考其独立文档调整代
类中提供了`compatible_openai`方法进行修改，为了尊重官网的demo我不考虑优先兼容模式，考虑兼容模式可以直接调用该方法

## 专属指令
考虑到deepseek的回答是markdown语法会有冲突（`# 指令内容`）就不采用 #空格指令了，直接把空格去掉（`#指令内容`）。
- `#R1`此次对话切换为R1模型
- `#V3`此次对话切换为V3模型
- `#R1-long`10轮对话保持R1模型
- `#V3-long`3轮对话保持V3模型
- `#R1-all`一直使用R1模型，对话记录一直保存
- `#V3-all`一直使用V3模型，对话记录保持在5轮以内0
- `#新对话`清空对话历史
- 

## 输出格式
输出默认全文本输出，不会带有markdown语法，如:
```markdown
markdown
# Hello World
**这里是加粗字体**
***这里是加粗和斜体***
```
只有在输出代码或必要的文本创作(表示word的表格)才会用上mrakdown。

**可以在提问的时候指定输出格式，如`json`、`markdown`、 `text`等，结合参数`response_format`能确保生成格式如：**
```python
问题：请生成json格式的文本
set_response_format("json_object")    # 调用方法修改response_format属性强制输出json格式的回答
# response_format = "text" 默认 
```

## 开发随笔
高并发，多线程，多进程
1.常规对话5轮清空，保持开头人物设定和预览回答（V3）
2.内容生成、多模态任务、智能客服、快速响应（V3）
3.技术、学科（数学）问题问答：保持全增量上下文对话（R1）
4.复杂推理10轮对话（R1）
5.怼人模式（R1）全增量
输入的量是有限制的，如果一条对话算100-400KB，内存溢出也得要等100万次对话，根本限制是官方的限制
6.保留原始的API接口对话，没有任何的人设直接回答

V3提供转换R1的方法，正常调用后直接转回V3，提供特殊指令之后一直是R1，超过一定时间不调用变V3（忘记关闭R1的情况）。

创建对象的时候可以指定默认使用什么模型，行是什么样的策略？

确保单一对象同一时刻只有一个模型，V3或R1

## API请求参数
1. **对话补全**：https://api-docs.deepseek.com/zh-cn/api/create-chat-completion  
***共15个参数：***  
`messages`、`model`、`frequency_penalty`、`max_tokens`、`presence_penalty`、`response_format`、`stop`、`stream`、`stream_options`、`temperature`、`top_p`、`tools`、`tool_choice`、`logprobs`、`top_logprobs`

<br>

2. **FIM补全**：https://api-docs.deepseek.com/zh-cn/api/create-chat-completion  
***共13个参数：***  
`model`、`prompt`、`echo`、`frequency_penalty`、`logprobs`、`max_tokens`、`presence_penalty`、`stop`、`stream`、`stream_options`、`suffix`、`temperature`、`top_p`

区别：
|对话补全| 1 |
| --- | --- |
|FIM补全| 1|
```python
# 模型默认V3(deepseek-chat)，R1是(deepseek-reasoner)
self.model_choice = "deepseek-chat"
# 介于 -2.0 和 2.0 之间的数字。如果该值为正，那么新 token 会根据其在已有文本中的出现频率受到相应的惩罚，降低模型重复相同内容的可能性。
self.frequency_penalty = 0  # 默认0
# 介于 1 到 8192 间的整数，限制一次请求中模型生成 completion 的最大 token 数。输入 token 和输出 token 的总长度受模型的上下文长度的限制。
self.max_tokens = 4096 #  默认4096个token（6825.667个字），8192为13653.33个字
# 介于 -2.0 和 2.0 之间的数字。如果该值为正，那么新 token 会根据其是否已在已有文本中出现受到相应的惩罚，从而增加模型谈论新主题的可能性。
self.presence_penalty = 0   # 默认0
# response_format。一个 object，指定模型必须输出的格式。设置为 { "type": "json_object" } 以启用 JSON 模式，该模式保证模型生成的消息是有效的 JSON。
self.response_format = {"type": "text"}   # 默认为text，{"type": "json_object"}强制 JSON 输出
# 停止生成标志词，string 或最多包含 16 个 string 的 list。比如","则在生成这个字符 前 就停止生成
self.stop = None
# 是否流式输出。如果设置为 True，将会以 SSE（server-sent events）的形式以流式发送消息增量。消息流以 data: [DONE] 结尾。
self.stream = False
# 只有在stream参数为true时才可设置此参数。如果设置为true，在流式消息最后的data: [DONE] 之前将会传输一个额外的块。此块上的 usage 字段显示整个请求的 token 使用统计信息
self.stream_options = {"include_usage": True} # 请求用量统计
# temperature 参数默认为(1.0)代码生成/数学解题(0.0)数据抽取/分析(1.0)通用对话(1.3)翻译(1.3)创意类写作/诗歌创作(1.5)
self.temperature = 1.3  # 默认日常聊天就设置为1.3了
# 作为调节采样温度的替代方案，模型会考虑前 top_p 概率的 token 的结果。所以 0.1 就意味着只有包括在最高 10% 概率中的 token 会被考虑。 我们通常建议修改这个值或者更改 temperature，但不建议同时对两者进行修改。
self.top_p = 1 # 默认值为1
# 模型可能会调用的 tool 的列表。目前，仅支持 function 作为工具。使用此参数来提供以 JSON 作为输入参数的 function 列表。最多支持 128 个 function。
self.tools = None   # 默认为None
# 控制模型调用 tool 的行为。
self.tool_choice  = "none"
# 是否返回所输出 token 的对数概率。如果为 true，则在 message 的 content 中返回每个输出 token 的对数概率。
self.logprobs = False
# 一个介于 0 到 20 之间的整数 N，指定每个输出位置返回输出概率 top N 的 token，且返回这些 token 的对数概率。指定此参数时，logprobs 必须为 true。
self.top_logprobs = None
```

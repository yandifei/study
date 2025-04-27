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
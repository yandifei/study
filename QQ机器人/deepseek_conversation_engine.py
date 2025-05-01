"""管理API的类(对话和余额计算等)
1.密钥安全读取和校验
2.多模式对话管理（V3/R1）
3.温度参数动态调节
4.Token消耗精准计算
5.API资源监控预警
"""
# 内置库
import os   # 导入系统库
from itertools import count

# 第三方库
import requests # 导入网络请求的库
import json # 解析服务器的json文本回应
import transformers # (爆红没事，能跑就行)
from openai import OpenAI,OpenAIError  # 导入OpenAI和OpenAI错误类型

class DeepseekConversationEngine:
    def __init__(self,role=None):
        """初始化DeepseekConversationEngine
        参数：role ： 对话人设，这个可以选择默认值None(提示库下的文件名)
        """
        self.__DEEPSEEK_API_KEY = self.__get_check_key()    # 从`系统环境变量中读入密钥和检查密钥
        """-----------------------------------------------------核心业务-----------------------------------------------------"""
        self.base_url ="https://api.deepseek.com"   # api网址
        """对话补全请求参数(回答内容控制)"""
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
        self.stream_options = None # 请求用量统计(必须开启流式输出才能开)
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
        """FIM对话补全参数"""
        # 用于生成完成内容的提示(需要补 全的开头)
        self.prompt = None
        # 在输出中，把 prompt 的内容也输出出来
        self.echo = False
        # 制定输出中包含 logprobs 最可能输出 token 的对数概率，包含采样的 token。
        self.FIM_logprobs = 0
        # 制定被补 全内容的后缀。
        self.suffix = None
        """历史对话处理"""
        self.reasoning_content = ""   # 保存最近一次的思维链
        self.clear_flag = 5 # 对话历史最大数，超过就清空最开始的那一次的对话(V3默认为5轮)
        self.dialog_history = list()    # 对话历史，列表存储(这个对话历史其实就是message参数)
        self.role = None    # 用来存放当前人设(不知道当前人设的时候可以调用输出展示)
        if role is not None:    # 人设不为空
            self.role = self.role_read(role)  # 读取人设
            self.dialog_history.append({"role": "system", "content": self.role})   # 添加人设
        # 记得设置没有任何人设的对话
        """余额查询"""
        self.balance_inquiry_url = "https://api.deepseek.com/user/balance"  # 余额查询网址
        """Token分词和计算"""
        # add_special_tokens=True是模型输入格式要求,False是纯文本Token计算
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("./deepseek_v3_tokenizer/",trust_remote_code=True)


    """密钥安全读取和校验"""
    @staticmethod
    def __get_check_key():
        """私有方法（从系统环境变量中读入密钥和检查密钥）密钥有效就进行属性修改"""
        try:
            # 从环境变量获取密钥
            DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']  # 从环境变量读取deepseek的api密钥
        except KeyError:
            raise KeyError(f"未在环境变量中找到deepseek的api密钥，请确保添加成功，如果确认已经添加请重启pycharm或该程序")
        import requests
        # 测试请求到模型列表端点
        response = requests.get(
            "https://api.deepseek.com/user/balance",  # 请求网址
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}  # 请求头
        )
        if response.status_code != 200:  # 检查响应状态码
            raise ValueError("API密钥无效或未授权，检查密钥是否正确或重启pycharm或程序")
        return DEEPSEEK_API_KEY

    """对话输出参数"""
    def compatible_openai(self):
        """修改属性self.base_url对OpenAI进行兼容
        # 出于与 OpenAI 兼容考虑，您也可以将 base_url 设置为 https://api.deepseek.com/v1 来使用，
        但注意，此处 v1 与模型版本无关。
        """
        self.base_url = "https://api.deepseek.com/v1"

    def use_beat(self):
        """修改self.base_url属性为"https://api.deepseek.com/beta"来开启api某些限制功能
        部分功能必须是beat才能开启，如R1思维返回就必须使用这个url"""
        self.base_url = "https://api.deepseek.com/beta"

    # 对话补充
    def switch_model(self):
        """模型切换，如果为 V3 模型就切换为 R1模型， 如果为 R1 模型则切换为 V3模型
        # 模型默认V3(deepseek-chat)，R1是(deepseek-reasoner)
        """
        if self.model_choice == "deepseek-chat":  # V3模型
            self.model_choice = "deepseek-reasoner" # R1模型
            self.clear_flag = 10  # 对话历史最大数，超过就清空最开始的那一次的对话(R1默认为10轮)
        else:
            self.model_choice = "deepseek-chat" # V3模型
            self.clear_flag = 5  # 对话历史最大数，超过就清空最开始的那一次的对话(V3默认为5轮)

    def set_frequency_penalty(self,frequency_penalty=0.0):
        """控制生成内容的重复性 -2.0（鼓励重复）到 2.0（严格避免重复）、0（无惩罚）
       在新 token 会根据其在已有文本中的出现频率受到相应的惩罚，降低模型重复相同内容的可能性。
       参数：frequency_penalty ： 默认0.0
       返回值：修改错误返回False，成功修改返回True
       """
        if frequency_penalty < -2 or frequency_penalty > 2:
            print("\033[91m参数不在有效范围内(-2.0至2.0)，不对该参数进行任何修改\033[0m")
            return False
        self.frequency_penalty = frequency_penalty
        return True

    def set_max_tokens(self,max_tokens=4096):
        """修改输出最大token数(1-8192)
        参数 ： max_tokens ： 默认4096个token（6825.667个字），8192个token为13653.33个字
        返回值：修改错误返回False，成功修改返回True
        """
        if max_tokens < 1 or max_tokens > 8192: # 不在1-8192的范围内
            print("\033[91m参数不在范围内(1-8192)，不对该参数进行任何修改\033[0m")
            return False
        self.max_tokens = max_tokens
        return True

    def set_presence_penalty(self,presence_penalty):
        """对模型的回答进行打分
        # 介于 -2.0 和 2.0 之间的数字。
        如果该值为正，那么新 token 会根据其是否已在已有文本中出现受到相应的惩罚，从而增加模型谈论新主题的可能性。
        参数： presence_penalty ： 默认 "text",字符串格式，可填"json"
        返回值：修改错误返回False，成功修改返回True
        """
        if presence_penalty < -2 or presence_penalty > 2:
            print(f"\033[91m参数有误，打分范围在-2.0到2.0之间，不对该参数进行任何修改\033[0m")
            return False
        self.presence_penalty = presence_penalty
        return True

    def set_response_format(self,response_format="text"):
        """指定模型必须输出的格式("text"或"json")
        参数： response_format ： 默认 "text",字符串格式，可填"json"
        返回值：修改错误返回False，成功修改返回True
        """
        if response_format == "text" or response_format == "json":
            self.response_format = response_format
            return True
        print(f"\033[91m参数有误，指定模型必须输出的格式为\"text\"或\"json\"，不对该参数进行任何修改\033[0m")
        return False

    def set_stop(self,stop=None):
        """停止生成标志词
        参数： stop ： 可以是单个字符，也可以是字符组成的列表（最多16个元素）
        返回值：修改错误返回False，成功修改返回True
        """
        if stop is None:
            self.stop = None
            return True
        elif isinstance(stop, list) and len(stop) > 16:
            print("\033[91m参数有误，停止标志词最多16，不对该参数进行任何修改\033[0m")
            return False
        self.stop = stop
        return True

    def set_stream(self,stream=False):
        """是否流式输出。如果设置为 True，将会以 SSE（server-sent events）的形式以流式发送消息增量。消息流以 data: [DONE] 结尾。
        参数： stream ： 默认为False(不开启流式)
        返回值：修改错误返回False，成功修改返回True
        """
        if not isinstance(stream, bool):
            print("\033[91m参数有误，True或False，不对该参数进行任何修改\033[0m")
            return False
        self.stream = stream
        return True

    def set_stream_options(self,stream_options=None):
        """流式消息最后的data多一个usage 字段，这个字段包括token 使用统计信息
        参数： stream_options ： 默认为None(不返回这个usage 字段),只能填None或True
        """
        if stream_options is None:
            self.stream_options = None
            return True
        elif not self.stream:     # self.stream必须为True(开启流式才能开启这个选项)
            print("\033[91m必须先开启流式(stream)才能开启修改开启这个字段\033[0m")
            return False
        elif not isinstance(stream_options, bool):
            print("\033[91m参数有误，True或False，不对该参数进行任何修改\033[0m")
            return False
        self.stream_options = {"include_usage": True}
        return True

    def set_temperature(self,temperature=1.0):
        """设置模型对话的温度
        参数 ： temperature ： 温度参数。直接调用就是设置为1.0
        默认为(1.0)代码生成/数学解题(0.0)数据抽取/分析(1.0)通用对话(1.3)翻译(1.3)创意类写作/诗歌创作(1.5)
        返回值：如果修改成功返回True，否则返回False
        """
        if temperature < 0.0 or temperature > 2.0:
            print("\033[91m超出温度范围(0.0-2.0),不对该参数进行任何修改.0\033[0m")
            return False
        else:
            self.temperature = temperature
            return True

    def set_top_p(self,top_p=1):
        """作为调节采样温度的替代方案，模型会考虑前 top_p 概率的 token 的结果。
        所以 0.1 就意味着只有包括在最高 10% 概率中的 token 会被考虑。我们通常建议修改这个值或者更改 temperature，但不建议同时对两者进行修改。
        参数： top_p ： 默认为1(0-1)
        返回值：如果修改成功返回True，否则返回False
        """
        if top_p < 0 or top_p > 1:
            print("\033[91m参数不在调用范围(0-1),不对该参数进行任何修改\033[0m")
            return False
        self.top_p = top_p
        return True

    def set_tools(self,tools=1):
        """模型可能会调用的 tool 的列表。目前，仅支持 function 作为工具。使用此参数来提供以 JSON 作为输入参数的 function 列表。最多支持 128 个 function。
        参数： tools ： 1-128
        返回值：如果修改成功返回True，否则返回False
        """
        if tools < 1 or tools > 128:
            print("\033[91m参数不在调用范围(1-128),不对该参数进行任何修改\033[0m")
            return False
        self.tools = tools
        return True

    def set_tool_choice(self,tool_choice="none"):
        """控制模型调用 tool 的行为。
        none 意味着模型不会调用任何 tool，而是生成一条消息。
        auto 意味着模型可以选择生成一条消息或调用一个或多个 tool。
        参数 ： tool_choice ： 默认"none"，有工具时填入"auto"
        返回值：如果修改成功返回True，否则返回False
        """
        if tool_choice != "none" or tool_choice != "auto":
            print("\033[91m参数错误,有工具为\"auto\"无工具为\"none\",不对该参数进行任何修改\033[0m")
            return False
        self.tool_choice = "none"
        return True

    def set_logprobs(self,log_probs=False):
        """是否返回所输出 token 的对数概率。如果为 true，则在 message 的 content 中返回每个输出 token 的对数概率。
        参数：log_probs ： 默认False
        返回值：如果修改成功返回True，否则返回False
        """
        if not isinstance(log_probs,bool):
            print("\033[91m参数错误,参数不是True或False,不对该参数进行任何修改\033[0m")
            return False
        self.logprobs = log_probs
        return True

    def set_top_logprobs(self,top_logprobs=None):
        """一个介于 0 到 20 之间的整数 N，指定每个输出位置返回输出概率 top N 的 token，且返回这些 token 的对数概率。
        指定此参数时，logprobs 必须为 true。
        参数：top_logprobs ： 默认为None
        返回值：如果修改成功返回True，否则返回False
        """
        if top_logprobs is None:
            self.top_logprobs = None
            return True
        elif not self.logprobs:
            print("\033[91m无效修改，必须当self.logprobs为True才能修改\033[0m")
            return False
        elif top_logprobs < 0 or top_logprobs > 20:
            print("\033[91m参数不在调用范围(0-20),不对该参数进行任何修改\033[0m")
            return False
        self.top_logprobs = top_logprobs
        return True

    # FIM补充
    def set_echo(self,echo):
        """在输出中，把 prompt 的内容也输出出来
        参数：echo : 默认False,
        返回值：返回True
        """
        if echo:
            self.echo = None    # 因为服务器那边不接受True，只接受False和None
        self.echo = True
        return True

    def set_FIM_logprobs(self,FIM_logprobs):
        """制定输出中包含 logprobs 最可能输出 token 的对数概率，包含采样的 token。最大20
        参数：FIM_logprobs : 默认0,最大20
        返回值：如果修改成功返回True，否则返回False
        """
        if FIM_logprobs < 0 or FIM_logprobs > 20:
            print("\033[91m参数不在调用范围(0-20),不对该参数进行任何修改\033[0m")
            return False
        self.FIM_logprobs = FIM_logprobs
        return True

    """多模式对话管理(核心业务)"""
    @staticmethod
    def role_read(txt_file_name):
        """提示库角色设定读取
        参数：txt_file_name ： txt文本文件名字(默认放在“提示库”的文件夹中)，不需要填后缀名
        返回值 ： role_information : 文本文件的内容
        """
        while True:
            txt_file_name += ".txt"  # 补足后缀名
            path = os.path.join("./提示库/", txt_file_name)
            if not os.path.isfile(path):  # 检查是否有这个文件（文件不存在）
                print(
                    f"\033[91m\"{os.path.join(os.getcwd(), "提示库")}\"中没有“{txt_file_name}”这个文件，请检查该txt文件是否存在\033[0m")
                txt_file_name = input("\033[92m请重新输入文件名(不用输入全名，路径自动补足)：\033[0m")
            else:  # 检查是否有这个文件（文件存在）:
                break  # 跳出循环
        with open(path, "r", encoding="utf-8") as role_txt:
            return role_txt.read()

    def add_role(self,role_txt):
        """添加角色扮演的提示（提示库 ）
        参数： role_txt : 角色扮演词
        """
        self.dialog_history.append({"role": "system", "content": role_txt})

    def add_answer(self,answer):
        """添加deepseek回答记录
        参数： answer ： AI回答文本
        """
        self.dialog_history.append({"role": "assistant", "content": answer})

    def add_question(self,question):
        """添加用户提出的问题
        参数： question ： 用户的问题
        """
        self.dialog_history.append({"role": "user", "content": question})

    def ask(self,ask_content):
        """用户发起提问
        参数 ： ask_content ： 用户提问的内容
        返回值：assistant_content  ： 返回AI回答的结果
        """
        # 把用户的问题添加的历史记录里面去
        self.dialog_history.append({"role": "user", "content": ask_content})
        try:
            client = OpenAI(api_key=self.__DEEPSEEK_API_KEY, base_url=self.base_url)
            response = client.chat.completions.create(
                messages = self.dialog_history,
                model=self.model_choice,
                frequency_penalty = self.frequency_penalty,
                max_tokens = self.max_tokens,
                presence_penalty = self.presence_penalty,
                response_format = self.response_format,
                stop = self.stop,
                stream = self.stream,  # 是否流式输出(是否逐字输出)
                stream_options = self.stream_options,
                temperature = self.temperature,
                top_p = self.top_p,
                tools = self.tools,
                tool_choice = self.tool_choice,
                logprobs = self.logprobs,
                top_logprobs = self.top_logprobs
            )
            self.reasoning_content = ""  # 每次调用后都清空之前思维链(R1的推理内容)[确保最近一次对话存在思维链]
            assistant_content = ""  # 临时文本(记录或拼接)
            if not self.stream: # 非流式输出记录
                print(response.choices[0].message.content)
                assistant_content = response.choices[0].message.content
                self.dialog_history.append({"role": "assistant", "content": assistant_content}) # 把AI的回答添加到对话记录里面去
                if self.model_choice == "deepseek-reasoner":     # R1模型会产生思维链（存在推理内容）
                    self.reasoning_content = response.choices[0].message.reasoning_content  # 把非流式的思维链接进行保存
            else:   #流式输出
                if self.model_choice == "deepseek-reasoner":     # R1模型会产生思维链（存在推理内容）
                    for chunk in response:  # 遍历流式返回的每个数据块
                        # 确保流式中返回的空数据块(None)不会影响输出就加or ""
                        print(f"{chunk.choices[0].delta.content or ""}", end="", flush=True)  # 实时逐词输出
                        assistant_content += chunk.choices[0].delta.content or "" # 累积最终回答
                        self.reasoning_content += chunk.choices[0].delta.reasoning_content or "" # 累积推理过程
                else:   # V3模型没有思维链
                    for chunk in response:  # 遍历流式返回的每个数据块
                        # 确保流式中返回的空数据块(None)不会影响输出就加or ""
                        print(f"{chunk.choices[0].delta.content or ""}", end="", flush=True)  # 实时逐词输出
                        assistant_content += chunk.choices[0].delta.content or "" # 累积最终回答
                print() # 打印换行
            self.dialog_history.append({"role": "assistant", "content": assistant_content}) # 添加AI的回答历史
            return assistant_content    # 返回AI回答的结果
        except OpenAIError as Error:
            # 获取 HTTP 状态码
            status_code = Error.status_code
            # print(f"错误码: {status_code}")
            # 根据状态码处理不同错误
            if status_code == 400:
                print("\033[91m请求体格式错误，请根据错误信息提示修改请求体\033[0m")
            elif status_code == 401:
                print("\033[91mAPIkey错误，认证失败。请检查您的APIkey是否正确如没有APIkey请先创建APIkey\033[0m")
            elif status_code == 402:
                print("\033[91m账号余额不足，请确认账户余额，并前往充值页面进行充值\033[0m")
            elif status_code == 422:
                print("\033[91m请求体参数错误，请根据错误信息提示修改相关参数\033[0m")
            elif status_code == 429:
                print("\033[91m请求速率（TPM 或 RPM）达到上限，请合理规划您的请求速率\033[0m")
            elif status_code == 500:
                print("\033[91m服务器内部故障，请等待后重试。若问题一直存在，请联系我们解决\033[0m")
            elif status_code == 503:
                print("\033[91m服务器负载过高，请稍后重试您的请求\033[0m")
            else:
                print(f"\033[91m未知错误: {Error}\033[0m")

    def fill_in_the_middle_ask(self,fim_prompt,fim_suffix):
        """FIM补 全（Beta）场景：代码补 全、文本填充（如生成函数逻辑、补 全模板中间内容）。
        精准填充文本中间的缺失部分（例如补 全函数体）。适合结构化内容生成（如代码、JSON）。
        注：只能单次对话，不具有上下文对话记录的功能
        参数： prompt，开头
        suffix，结尾
        返回值: response_content : 补 全对话后的内容(完整版)
        """
        try:
            client = OpenAI(api_key=self.__DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/beta")
            response = client.completions.create(
                model="deepseek-chat",
                prompt = fim_prompt,       # FIM补全特有
                echo = self.echo,           # FIM补全特有
                frequency_penalty = self.frequency_penalty,
                logprobs = self.FIM_logprobs,
                max_tokens = self.max_tokens,
                presence_penalty = self.presence_penalty,
                stop = self.stop,
                stream = self.stream,
                stream_options = self.stream_options,
                suffix = fim_suffix,       # FIM补全特有
                temperature = self.temperature,
                top_p = self.top_p
            )
            response_content = fim_prompt  # 流式回复内容拼接(默认拼接给的开头)
            if not self.stream:  # 非流式输出记录
                print(fim_prompt + response.choices[0].text + fim_suffix)
                response_content = response.choices[0].text + fim_suffix
            else:   # 流式输出
                print(fim_prompt, end="")   # 拼接开头
                for chunk in response:  # 遍历流式返回的每个数据块
                    print(f"{chunk.choices[0].text or ""}", end="", flush=True)  # 实时逐词输出
                    response_content += chunk.choices[0].text or "" # or "" 防止为None报错
                print(fim_suffix) # 拼接结尾和换行(使用流式输出后得换行)
                response_content += fim_suffix  # 拼接给的结尾
            return response_content # 返回回答后的问本
        except OpenAIError as Error:
            # 获取 HTTP 状态码
            status_code = Error.status_code
            # print(f"错误码: {status_code}")
            # 根据状态码处理不同错误
            if status_code == 400:
                print("\033[91m请求体格式错误，请根据错误信息提示修改请求体\033[0m")
            elif status_code == 401:
                print("\033[91mAPIkey错误，认证失败。请检查您的APIkey是否正确如没有APIkey请先创建APIkey\033[0m")
            elif status_code == 402:
                print("\033[91m账号余额不足，请确认账户余额，并前往充值页面进行充值\033[0m")
            elif status_code == 422:
                print("\033[91m请求体参数错误，请根据错误信息提示修改相关参数\033[0m")
            elif status_code == 429:
                print("\033[91m请求速率（TPM 或 RPM）达到上限，请合理规划您的请求速率\033[0m")
            elif status_code == 500:
                print("\033[91m服务器内部故障，请等待后重试。若问题一直存在，请联系我们解决\033[0m")
            elif status_code == 503:
                print("\033[91m服务器负载过高，请稍后重试您的请求\033[0m")
            else:
                print(f"\033[91m未知错误: {Error}\033[0m")

    def  dialog_history_manage(self):
        """多轮对话管理，判断是否删除最旧的一轮对话，V3是5轮，R1是10轮"""
        while int(len(self.dialog_history) / 2) > self.clear_flag:  # 超过对话轮次了
            if self.role is not None:   # 人设不为空的情况
                del self.dialog_history[1:3]    # 删除最开始的一轮对话(0是我人设(不能删)，1是我的提问，2是AI回答，不会到达3)
            else:   # 人设为空（没有设置人设）
                del self.dialog_history[0:2]    # 删除最开始的一轮对话(0是我的提问，1是AI回答，不会到达2)

    # def conversation_engine(self):
    #     """对话引擎
    #     实现对话交流的方法(模型切换的逻辑都在里面)
    #     """
    #     while True:
    #         input("我：")  # 输入你的发言



    """余额计算和监控"""
    def balance_inquiry(self, out=False):
        """查询deepseek的API余额
        参数：
        DEEPSEEK_API_KEY ： API密钥
        out : 是否对返回值进行打印
        返回值：返回一个列表
        0 ： 布尔值（余额是否充足）
        1 ： 字符串型（货币类型）
        2 : 字符串型（总的可用余额(包括赠金和充值余额)）
        3 ： 未过期的赠金余额
        4 ： 充值余额
        """
        return_list = list()  # 返回值的列表
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.__DEEPSEEK_API_KEY}'  # 密钥
        }
        response = requests.request("GET", self.balance_inquiry_url, headers=headers, data={})  # 发送查询请求
        data = json.loads(response.text)  # 解析json数据，(必须使用json库，本身就是文本格式和避免陷阱)
        if data["is_available"]:  # 如果为True
            return_list.append(True)
            if out: print("\033[92m余额充足，api可以调用\033[0m", end="\t")
        elif not data["is_available"]:  # 如果为False
            return_list.append(False)
            if out: print("\033[91m余额不足，api无法调用\033[0m", end="\t")
        detail_list = data["balance_infos"]  # 详细信息
        currency_type = ""  # 货币类型放置
        if detail_list[0]["currency"] == "CNY":  # 人民币
            return_list.append("元")
            currency_type = "元"  # 货币类型为人民币
        elif detail_list[0]["currency"] == "USD":  # 美元
            return_list.append("美元")
            currency_type = "美元"  # 货币类型为美元
        return_list.append(detail_list[0]["total_balance"])
        return_list.append(detail_list[0]["granted_balance"])
        return_list.append(detail_list[0]["topped_up_balance"])
        if out:
            print(f"总的可用余额(包括赠金和充值余额):{detail_list[0]["total_balance"]}{currency_type}", end="\t")
            print(f"未过期的赠金余额:{detail_list[0]["granted_balance"]}{currency_type}", end="\t")
            print(f"充值余额:{detail_list[0]["topped_up_balance"]}{currency_type}")
        return return_list

    def calculate_token_capacity(self, out=False):
        """计算余额可用token和字数
        参数：
        DEEPSEEK_API_KEY ： API密钥
        out : 是否对返回值进行打印
        返回值：返回一个列表
        min_token : 可用token数
        characters ： 最少的中文字符字数(直接取整数)
        words ： 最少的英文字符字数(直接取整数)
        round(((characters*24)/1024)/1024,2)  ： 最少可生产的数据(GB)
        round(characters/880000,2)  : 约几本《三体》(88万字一本)
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.__DEEPSEEK_API_KEY}'  # 密钥
        }
        response = requests.request("GET", self.balance_inquiry_url, headers=headers, data={})  # 发送查询请求
        data = json.loads(response.text)  # 解析json数据，(必须使用json库，本身就是文本格式和避免陷阱)
        detail_list = data["balance_infos"]  # 详细信息
        min_token = float(detail_list[0]["total_balance"]) * 62500  # 当前金额(元) * 62500[每元的token数]
        characters = int(min_token / 0.6)  # 最少的中文字符字数(直接取整数)
        words = int(min_token / 0.3)  # 最少的英文字符字数(直接取整数)
        if out:
            print(
                f"当前可用余额能生成最少 {int(min_token)} token，对话可使用最少约{characters}个汉字，对话可使用最少约{words}英文字符")
            print(
                f"最少可生产:{round(((characters * 24) / 1024) / 1024, 2)}GB 的对话数据， 约{round(characters / 880000, 2)}本《三体》(88万字一本)")
        return min_token, characters, words, round(((characters * 24) / 1024) / 1024, 2), round(characters / 880000, 2)

    """Token分词和计算"""
    def calculate_token(self,input_text, out=False):
        """计算总的token数
        参数：
        input_text ： 需要计算token的文本
        out ： 默认为False，是否输出过程信息
        返回值：输入文本的token数
        """
        # add_special_tokens=False标记仅编码原始文本内容纯文本Token计算
        result = self.tokenizer.encode(input_text, add_special_tokens=False)
        if out:
            print(f"输入的文本：{input_text}")
            # print(tokenizer.convert_ids_to_tokens([30594, 303, 3427, 3])) # 转义回去
            print(f"Token 数量: {len(result)}")
        return len(result)

    def token_ids(self,input_text, out=False):
        """使用分词器将符号转换为ID
        参数：
        input_text  ： 需要转为ID的文本
        out ： 默认为False，是否输出过程信息
        返回值：字符ID序列组
        """
        result = self.tokenizer.encode(input_text, add_special_tokens=False)
        if out:
            print(f"输入的文本：{input_text}")
            print(f"字符ID序列组: {result}")
        return result

    def restore_text(self,input_text, out=False):
        """token分词转文本
        参数：
        input_text ： 一个包含 token ID 的列表（数组类型）
        out ： 默认为False，是否输出过程信息
        返回值：文本
        """
        # print(tokenizer.decode([30594, 303, 3427, 3])) # 转义回去
        result = self.tokenizer.decode(input_text)
        if out:
            print(f"输入token ID 的列表：{input_text}")
            print(f"还原的文本:{result}")
        return result

if __name__ == '__main__':
    deepseek = DeepseekConversationEngine(None)  # 实例化对象(人设为专属猫娘)
    deepseek.switch_model()  # 切换R1模型(默认V3模型)
    deepseek.set_stream(True)   # 设置流式输出
    deepseek.clear_flag = 2 # 设置对话轮次为2轮
    count = 0   # 对话轮次记录
    while True:
        count += 1                           # 对话轮次数
        print(f"{'第'+ str(count) + '对话':-^123}")  # 画一条线
        deepseek.ask(input("我:"))           # 接收我的发言并进行处理
        deepseek.dialog_history_manage()     # 自动清理最旧的对话记录
        print(f"{'历史记录':-^123}")          # 画一条线
        print(deepseek.dialog_history)       # 输出历史记录




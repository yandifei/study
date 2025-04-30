"""管理API的类(对话和余额计算等)
1.密钥安全读取和校验
2.多模式对话管理（V3/R1）
3.温度参数动态调节
4.Token消耗精准计算
5.API资源监控预警
"""
# 内置库
import os   # 导入系统库
# 第三方库
import requests # 导入网络请求的库
import json # 解析服务器的json文本回应
import transformers # (爆红没事，能跑就行)
from openai import OpenAI,OpenAIError  # 导入OpenAI和OpenAI错误类型

class DeepseekConversationEngine:
    def __init__(self):
        self.__DEEPSEEK_API_KEY = self.__get_check_key()    # 从`系统环境变量中读入密钥和检查密钥
        """-----------------------------------------------------核心业务-----------------------------------------------------"""
        self.base_url ="https://api.deepseek.com"   # api网址
        self.role = self.role_read("编程教师")
        """请求参数(回答内容控制)"""
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
        """历史对话处理"""
        self.dialog_history = list()    # 对话历史，列表存储
        self.clear_flag = 5 # 对话历史最大数，超过就清空最开始的那一次的对话(V3默认为5轮)
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

    def set_model(self):
        """模型切换，如果为 V3 模型就切换为 R1模型， 如果为 R1 模型则切换为 V3模型
        # 模型默认V3(deepseek-chat)，R1是(deepseek-reasoner)
        """
        if self.model_choice == "deepseek-chat":  # V3模型
            self.model_choice = "deepseek-reasoner" # R1模型
        else:
            self.model_choice = "deepseek-chat" # V3模型

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

    def set_temperature(self,temperature):
        """设置模型对话的温度
        参数 ： temperature ： 温度参数
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
        elif top_logprobs is not None or not top_logprobs:
            print("\033[91m参数错误，参数为True或None，不对该参数进行任何修改\033[0m")
            return False
        self.top_logprobs = top_logprobs
        return True

    """多模式对话管理(核心业务)"""
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

    def ask(self,ask_txt):
        """发起提问
        """
        try:
            client = OpenAI(api_key=self.__DEEPSEEK_API_KEY, base_url=self.base_url)
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.role},  # 系统提示（设定角色）"
                    # {"role": "assistant", "content": "我已准备就绪"},  # 系统提示（设定角色）"
                    {"role": "user", "content": ask_txt},  # 用户输入
                ],
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
            print(response.choices[0].message.content)
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
                print(f"\033[91m未知错误: {e}\033[0m")

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
    deepseek = DeepseekConversationEngine()
    deepseek.role = deepseek.role_read("变态猫娘")
    deepseek.ask("我要睡午觉了")
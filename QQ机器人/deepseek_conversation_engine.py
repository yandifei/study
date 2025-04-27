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
from openai import OpenAI

class DeepseekConversationEngine:
    def __init__(self):
        self.__DEEPSEEK_API_KEY = self.__get_check_key()    # 从`系统环境变量中读入密钥和检查密钥
        """核心业务"""
        self.client = OpenAI(api_key=self.__DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        self.model_choice = "deepseek-chat" # 模型默认V3(deepseek-chat)，R1是(deepseek-reasoner)
        # temperature 参数默认为(1.0)代码生成/数学解题(0.0)数据抽取/分析(1.0)通用对话(1.3)翻译(1.3)创意类写作/诗歌创作(1.5)
        self.temperature = 1.3 # 默认日常聊天就设置为1.3了
        self.dialog_history = list()    # 对话历史，列表存储
        self.clear_flag = 5 # 对话历史最大数，超过就清空最开始的那一次的对话(V3默认为5轮)
        # 记得设置没有任何人设的对话
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

    """多模式对话管理(核心业务)"""
    def compatible_openai(self):
        """修改self.client属性中的base_url对OpenAI进行兼容
        # 出于与 OpenAI 兼容考虑，您也可以将 base_url 设置为 https://api.deepseek.com/v1 来使用，
        但注意，此处 v1 与模型版本无关。
        """
        self.client = OpenAI(api_key=self.__DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")

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
        url = "https://api.deepseek.com/user/balance"  # 余额查询网址
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.__DEEPSEEK_API_KEY}'  # 密钥
        }
        response = requests.request("GET", url, headers=headers, data=payload)  # 发送查询请求
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
        url = "https://api.deepseek.com/user/balance"  # 余额查询网址
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.__DEEPSEEK_API_KEY}'  # 密钥
        }
        response = requests.request("GET", url, headers=headers, data=payload)  # 发送查询请求
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
    a = DeepseekConversationEngine()
    # a.calculate_token("Hello world",True)
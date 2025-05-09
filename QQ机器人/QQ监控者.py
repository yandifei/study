from QQScript.QQMessageMonitor import * # 导包
from deepseek_conversation_engine import DeepseekConversationEngine
import sys
import types
"""--------------------------------------------------需要修改的参数----------------------------------------------------"""
# qq_group_name = input("请输入监听的群聊:\n") # 猫猫       雁低飞
# qq_monitor_name = input("请输入你的身份(最好是聊天对象的名称，如你在q群的名称):\n")
qq_group_name = "1"
qq_monitor_name = "猫猫"
administrator = ["雁低飞","yandifei"]  # 设置超级管理员
role = "变态猫娘"   # (设置人设为专属猫娘)编程教师
"""--------------------------------------------------QQ窗口绑定处理----------------------------------------------------"""
chat_win1 = QQMessageMonitor(qq_group_name, qq_monitor_name)    # 会自动置顶和自动展示(最小化显示)
chat_win1.show_win()    # 展示窗口
chat_win1.top_win()     # 置顶窗口
# chat_win1.cancel_top_win()  # 取消置顶
chat_win1.move()        # 把窗口移动到最上角 0,1010
print("窗口已放置最左上角并置顶，可通过鼠标拖拽拉伸")
print(f"数据存放路径:\t{chat_win1.message_data_txt}")
for one_message in chat_win1.message_list:  # 打印初次绑定后的消息
    print(one_message)
"""-------------------------------------------------QQ消息监快捷指令----------------------------------------------------"""
def exit_qq_auto_reply(administrator_name):
    """判断是否退出QQ自动回复
    参数 ： administrator_name ： 超级管理员的名字
    """
    if administrator_name in administrator:
        print("\033[31m已停止QQ监听回复和退出deepseek对话引擎\033[0m")
        chat_win1.send_message("已停止QQ自动回复\n已退出deepseek对话引擎")
        sys.exit()  # 优雅退出程序
    else:
        print("\033[31m此为高级操作，你无权执行该指令\033[0m")
        chat_win1.send_message("此为高级操作，你无权执行该指令")
"""----------------------------------------------------deepseek接入----------------------------------------------------"""
deepseek = DeepseekConversationEngine(role)  # 实例化对象
# deepseek.set_stream(True)  # 设置流式输出
def qq_input(order,args_tips):
    """QQ指令接收和参数提示
    参数：order ： 接收的指令
    args_tips ： 提示的内容
    返回值 ： order
    """
    chat_win1.send_message(args_tips)  # QQ发送接收参数提示内容
    return order


# 接收指令改处理过程：接收到修改的指令后发出提示，接收新的 请求参数
# 其实就是重写快捷指令
def qq_quick_order(order: str):
    """qq快捷指令（调用此方法后自动分割后通过关键字快速找到其他方法）
    参数： order ： 收到的消息(#R1模型)
    返回值：如果指令存在则执行对应的函数后返回True，如果指令不存在返回False
    """

    """-------------------------------------------指令解析-------------------------------------------"""
    # 函数映射表(使用lambda来匿名函数)
    function_map = {
        # 特殊指令
        "兼容": [lambda: deepseek.compatible_openai(),"已经切换至兼容OpenAI的接口","切换中途发生异常"],
        "测试接口": [lambda: deepseek.use_beat(),"已切换至测试接口","切换中途发生异常"],
        "初始化": [lambda: deepseek.reset(),"已格式化deepseek对话引擎","初始化中途发生异常"],  # 恢复最开始设置的参数（创建对象时的默认参数）
        # 对话参数调节指令
        "模型切换": [lambda: deepseek.switch_model(True),lambda : "已切换至V3模型" if deepseek.model_choice == "deepseek-chat" else "已切换至R1模型", "切换中途发生异常"],
        "V3模型": [lambda: deepseek.set_model("V3"),"已切换至V3模型", "切换中途发生异常"],
        "R1模型": [lambda: deepseek.set_model("R1"),"已切换至R1模型", "切换中途发生异常"],
        "评分": [lambda: deepseek.score_answer(score=50),"评分成功", "超出打分范围([0-100]分,默认50分)"],
        "最大token数": [lambda: deepseek.set_max_tokens(),f"已修改为{deepseek.max_tokens}", "超出最大token数范围([1-8192]分,默认4096)"],
        "输出格式": [lambda: deepseek.set_response_format(),f"已修改为{deepseek.response_format}格式", "格式有误，指定模型必须输出的格式为\"text\"或\"json\""],    # input("请输入指定输出格式(text或json,],默认text):")
        "敏感词": [lambda: deepseek.set_stop(),"添加成功","添加失败"],    # input("设置敏感词(默认为None):")
        "删除敏感词": [lambda : deepseek.del_stop(""),"删除成功","敏感词不存在"],
        "流式": [lambda: deepseek.set_stream(True),"已切换至流式输出","切换中途发生异常"],
        "非流式": [lambda: deepseek.set_stream,"已切换至流式输出", "切换中途发生异常"],
        "请求统计": [lambda: deepseek.set_stream_options(True),"已开启请求统计", "开启请求统计途中发生异常"],
        "关闭请求统计": [lambda: deepseek.set_stream_options(),"已关闭请求统计", "关闭请求统计途中发生异常"],
        "温度": [lambda: deepseek.set_temperature(),"修改成功", "超出温度范围([0.0-2.0]分,默认1.0)"],
        "核采样": [lambda: deepseek.set_top_p(),"修改成功", "超出温度范围([0.0-1.0]分,默认1.0)"],   # float(input("请输入核采样,],数值越小内容部分逻越严谨(0.0-1.0,],默认1.0):"))
        "工具列表": [lambda: deepseek.set_tools(),""],  # input("请输入模型可能会调用的 tool 的列表(默认为None):")
        "工具选择": [lambda: deepseek.switch_tool_choice(),],
        "开启对数概率输出": [lambda: deepseek.set_logprobs(True),],
        "关闭对数概率输出": [lambda: deepseek.set_logprobs,],
        "位置输出概率": [lambda: deepseek.set_top_logprobs(),],  # int(input("请指定的每个输出位置返回输出概率top为几的token(0-20，默尔为None):"))
        # FIM对话参数
        "补全开头": [lambda: deepseek.set_prompt(args),"已补全开头", "补全开头失败"],
        "完整输出": [lambda: deepseek.set_echo(),],  # 这个参数就只有False和None了，改不了一点
        "FIM对数概率输出": [lambda: deepseek.set_FIM_logprobs(),],  # int(input("请输入需要多少个候选token数量输出对数概率(默认0):"))
        "补全后缀": [lambda: deepseek.set_suffix(),"已补全后缀", "后缀补全失败"], # input("请输入需要补全的后缀(默认为None):")
        # 上下文参数
        "思维链": [lambda: deepseek.reasoning_content_output, lambda: deepseek.reasoning_content_output,"思维链为空"],  # 会返回False或字符串
        "对话轮次": [lambda: deepseek.set_dialog_history(), f"已设置对话轮次为{deepseek.clear_flag}轮", "设置对话轮次失败"], # int(input("请输入最大对话轮数，超过自动删除(默认值为5):"))
        "聊天记录": [lambda: deepseek.print_dialog_history(), lambda: deepseek.print_dialog_history(),"无法输出对话内容"],
        "清空对话历史": [lambda: deepseek.clear_dialog_history(),"已清空对话历史(人设除外)","清空途中异常"],
        # 多人设管理
        "人设切换": [lambda: deepseek.role_switch(args),"人设切换成功","人设切换失败"],    # input("请输入切换的人设:")
        "所有人设": [lambda: deepseek.role_list(),deepseek.role_list(), deepseek.role_list()],  # 人设做了处理
        "人设查询": [lambda: deepseek.select_role_content(args),deepseek.select_role_content(args), "人设查询失败"],    # input("请输入要查询的人设:")
        "当前人设": [lambda: deepseek.print_role_content(),deepseek.role,"人设为空"],
        "人设自定": [lambda: deepseek.set_role(args),"人设设定成功", "自定义人设失败"],# input("请输入人设内容:")
        "删除人设": [lambda: deepseek.remove_role(),"人设删除成功", "人设删除失败"],
        # 场景关键词自动调控参数
        "代码": [lambda: deepseek.scene_switch("代码"),"已切换至代码场景","切换场景失败"],
        "数学": [lambda: deepseek.scene_switch("代码"),"已切换至数学场景","切换场景失败"],
        "数据": [lambda: deepseek.scene_switch("数据"),"已切换至数据场景","切换场景失败"],
        "分析": [lambda: deepseek.scene_switch("分析"),"已切换至分析场景","切换场景失败"],
        "对话": [lambda: deepseek.scene_switch("对话"),"已切换至对话场景","切换场景失败"],
        "翻译": [lambda: deepseek.scene_switch("翻译"),"已切换至翻译场景","切换场景失败"],
        "创作": [lambda: deepseek.scene_switch("创作"),"已切换至创作场景","切换场景失败"],
        "写作": [lambda: deepseek.scene_switch("写作"),"已切换至写作场景","切换场景失败"],
        "作诗": [lambda: deepseek.scene_switch("作诗"),"已切换至作诗场景","切换场景失败"],
    }
    def execute_function(true_false_result):
        """是否执行返回值的函数
        参数 : true_false_result  ；执行结果
        """
        if true_false_result:  # 执行结果有效果
            if function_check(function_map[order][1]):  # 真值是一个函数
                chat_win1.send_message(function_map[order][1]())  # 执行真值的函数并发送
            else:
                chat_win1.send_message(function_map[order][1])  # 直接发送真值
        else:
            if function_check(function_map[order][2]):  # 假值是一个函数
                chat_win1.send_message(function_map[order][2]())  # 执行假值的函数并发送
            else:
                chat_win1.send_message(function_map[order][2])  # 直接发送假值

    # 用来放置参数(必须存在,需要用来判断是否需要参数)
    args = None
    function_check = lambda def_function: True if isinstance(def_function, types.LambdaType) else False   # 检查是否为匿名函数
    # 检查指令是否包含参数并做处理
    if ":" in order:  # 如何指令中存在:代表的是参数
        if order.split(":")[1]:     # 参数为空
            chat_win1.send_message("参数为空")
            return False
        order, args = order.split(":")[0], order.split(":")[1]  # 分割指令和参数
    # 检查指令是否在函数映射字典中
    if order not in function_map:   # 指令不在字典里面
        chat_win1.send_message("不存在该指令")
        print("\033[93m接收到了不存在的指令\033[0m")
        return False  # 没有这个指令
    else:
        if function_check(order) and args is None:   # 是一个无参函数
            result = function_map[order][0]()    # 执行函数并拿到返回结果
            execute_function(result)
        elif function_check(order) and args is not None:    # 是有参函数
            result = function_map[order][0](args)  # 传入参数并执行函数并拿到返回结果
            execute_function(result)
        else:   # 不是一个函数(可能是None、True、False)
            result = function_map[order][0]     # 传入的不是一个函数不执行，仅仅拿到值
            execute_function(result)
    return True  # 存在指令且执行即返回True

"""-------------------------------------------------QQ消息回复处理-----------------------------------------------------"""
while True:
    sleep(0.5)  # 每0.5秒监测一次变化
    chat_win1.show_win()    # 展示窗口
    chat_win1.top_win()     # 置顶开窗口
    chat_win1.monitor_message() # 始监控
    """消息处理"""
    if len(chat_win1.message_processing_queues) > 0:    # 队列不为空，进行队列处理
        # 这里是发送者的名字，我接收它的名字
        sender = chat_win1.message_processing_queues[0]["发送者"]
        # 我接受的消息（这里的发送消息指的是对方的发送消息)
        accept_message = chat_win1.message_processing_queues[0]["发送消息"]
        accept_message = accept_message.replace(f"@{chat_win1.monitor_name} ", "")   # 去除（@自己的名字 ）这个部分
        # 对方的消息发送时间
        accept_time = chat_win1.message_processing_queues[0]["发送时间"]

        """===============快捷指令处理==========="""
        if "#" == accept_message[0]:   # 检测到指令的消息
            if "#退出" in accept_message:      # 消息中存在退出指令
                exit_qq_auto_reply(sender)     # 检查发送者的身份是否为管理员(内置优雅退出)
            else: qq_quick_order(accept_message)    # 把指令带进入分析
            chat_win1.message_processing_queues.pop(0)  # 清理收到的指令(出队)
            print(f"\033[94m已完成“{sender}”的指令\033[0m")
        else:       # 非退出指令操作
            # deepseek.conversation_engine(content)  # 调用对话引擎
            reply = deepseek.ask(f"{sender}:{accept_message}",False)  # 发出请求并回应(这里不打印到屏幕上)
            print(f"\033[96m{reply}\033[0m")    # 打印回应字体(青色)
            chat_win1.send_message(f"@{sender}"+ reply)                       # 把回应发送到qq
            deepseek.dialog_history_manage()    # 自动删除久远的对话历史
            chat_win1.message_processing_queues.pop(0)  # 清理回应的消息(出队)
            print(f"\033[94m已完成“{sender}”的消息处理\033[0m")

# {"发送者": "yan di fei","发送消息": "hello world","发送时间": "10:10:20"}


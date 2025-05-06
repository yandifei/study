from itertools import count

from QQScript.QQMessageMonitor import * # 导包
from deepseek_conversation_engine import DeepseekConversationEngine
"""--------------------------------------------------QQ窗口绑定处理------------------------------------------------------"""
# qq_group_name = input("请输入监听的群聊:\n") # 猫猫       雁低飞
# qq_monitor_name = input("请输入你的身份(最好是聊天对象的名称，如你在q群的名称):\n")
qq_group_name = "鸣潮自动刷声骸"
qq_monitor_name = "猫猫"
chat_win1 = QQMessageMonitor(qq_group_name, qq_monitor_name)    # 会自动置顶和自动展示(最小化显示)
chat_win1.show_win()    # 展示窗口
# chat_win1.top_win()     # 置顶窗口
# chat_win1.cancel_top_win()  # 取消置顶
chat_win1.move(-579,5)        # 把窗口移动到最上角 0,1010
print("窗口已放置最左上角并置顶，可通过鼠标拖拽拉伸")
print(f"数据存放路径:\t{chat_win1.message_data_txt}")
for one_message in chat_win1.message_list:  # 打印初次绑定后的消息
    print(one_message)
"""----------------------------------------------------deepseek接入-----------------------------------------------------"""
deepseek = DeepseekConversationEngine("专属猫娘")  # 实例化对象(设置人设为专属猫娘)编程教师
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
def qq_quick_order(order):
    """qq快捷指令（调用此方法后可通过关键字快速找到其他方法）
    参数： order ： 字符串(设置的指令)
    返回值：如果指令存在则执行对应的函数后返回True，如果指令不存在返回False
    """
    # 函数映射表(使用lambda来匿名函数)
    function_map = {
        # 特殊指令
        "#兼容": lambda: deepseek.compatible_openai(),
        "#测试接口": lambda: deepseek.use_beat(),
        "#初始化": lambda: deepseek.__init__(),  # 恢复最开始设置的参数（创建对象时的默认参数）
        # 对话参数调节指令
        "#模型切换": lambda: deepseek.switch_model,
        "#V3模型": lambda: deepseek.set_model("V3"),
        "#R1模型": lambda: deepseek.set_model("R1"),
        "#打分": lambda: deepseek.score_answer(int(qq_input("对此次回答进行打分(0-100分,默认50分):"))),
        "#最大token": lambda: deepseek.set_max_tokens(int(input("请输入最大token限制(1-8192,默认4096):"))),
        "#输出格式": lambda: deepseek.set_response_format(input("请输入指定输出格式(text或json):")),
        "#敏感词": lambda: deepseek.set_stop(input("设置敏感词:")),
        "#流式": lambda: deepseek.set_stream(True),
        "#非流式": lambda: deepseek.set_stream,
        "#请求统计": lambda: deepseek.set_stream_options(True),
        "#关闭请求统计": lambda: deepseek.set_stream_options(),
        "#温度": lambda: deepseek.set_temperature(float(input("请输入温度,数值越小全文逻越严谨(0.0-2.0,默认1.0):"))),
        "#核采样": lambda: deepseek.set_top_p(float(input("请输入核采样,数值越小内容部分逻越严谨(0.0-1.0,默认1.0):"))),
        "#工具列表": lambda: deepseek.set_tools(input("请输入模型可能会调用的 tool 的列表(默认为None):")),
        "#工具选择": lambda: deepseek.switch_tool_choice(),
        "#开启对数概率输出": lambda: deepseek.set_logprobs(True),
        "#关闭对数概率输出": lambda: deepseek.set_logprobs,
        "#位置输出概率": lambda: deepseek.set_top_logprobs(
            int(input("请指定的每个输出位置返回输出概率top为几的token(0-20，默尔为None):"))),
        # FIM对话参数
        "#补全开头": lambda: deepseek.set_prompt(input("请输入需要补全的开头:")),
        "#完整输出": lambda: deepseek.set_echo(),  # 这个参数就只有False和None了，改不了一点
        "#FIM对数概率输出": lambda: deepseek.set_FIM_logprobs(
            int(input("请输入需要多少个候选token数量输出对数概率(默认0):"))),
        "#补全后缀": lambda: deepseek.set_suffix(input("请输入需要补全的后缀(可以不填):")),
        # 上下文参数
        "#思维链": lambda: deepseek.reasoning_content_output(),
        "#对话轮次": lambda: deepseek.set_dialog_history(int(input("请输入最大对话轮数(超过自动删除):"))),
        "聊天记录": lambda: deepseek.print_dialog_history(),
        "#清空对话历史": lambda: deepseek.clear_dialog_history(),
        # 多人设管理
        "#人设切换": lambda: deepseek.role_switch(input("请输入切换的人设:")),
        "#所有人设": lambda: deepseek.role_list(),
        "#人设查询": lambda: deepseek.select_role_content(input("请输入要查询的人设:")),
        "#当前人设": lambda: deepseek.print_role_content(),
        "#人设自定": lambda: deepseek.set_role(input("请输入人设内容:")),
        "#删除人设": lambda: deepseek.remove_role(),
        # 场景关键词自动调控参数
        "#代码": lambda: deepseek.scene_switch("代码"),
        "#数学": lambda: deepseek.scene_switch("数学"),
        "#数据": lambda: deepseek.scene_switch("数据"),
        "#分析": lambda: deepseek.scene_switch("分析"),
        "#对话": lambda: deepseek.scene_switch("对话"),
        "#翻译": lambda: deepseek.scene_switch("翻译"),
        "#创作": lambda: deepseek.scene_switch("创作"),
        "#写作": lambda: deepseek.scene_switch("写作"),
        "#作诗": lambda: deepseek.scene_switch("作诗")
    }
    if order in function_map:  # 检查指令是否在函数映射字典中
        function = function_map[order]  # 拿到映射的函数
        function()  # 执行映射的函数
        return True
    else:
        return False


"""-------------------------------------------------QQ消息监听和处理-----------------------------------------------------"""
while True:
    sleep(0.5)  # 每0.5秒监测一次变化
    chat_win1.show_win()    # 展示窗口
    chat_win1.top_win()     # 置顶开窗口
    chat_win1.monitor_message() # 始监控
    if len(chat_win1.message_processing_queues) > 0:    # 队列不为空，进行队列处理
        sender = chat_win1.message_processing_queues[0]["发送者"]          # 这里是发送者的名字，我接收它的名字
        accept_message = chat_win1.message_processing_queues[0]["发送消息"] # 我接受的消息（这里的发送消息指的是对方的发送消息）
        accept_time = chat_win1.message_processing_queues[0]["发送时间"]      # 对方的消息发送时间
        if "#退出" in chat_win1.message_processing_queues[0]["发送消息"]:      # 处理发送的消息(队头)
            if sender != "雁低飞":
                 chat_win1.send_message("此为高级操作，你无权执行该指令")
            else:
                chat_win1.send_message("已停止QQ监听回复和退出deepseek对话引擎")
                break   # 接收到的消息包括#退出就进行退出对话引擎
        else:       # 非退出指令操作
            # deepseek.conversation_engine(content)  # 调用对话引擎
            reply = deepseek.ask(f"{sender}:{accept_message}",False)  # 发出请求并回应(这里不打印到屏幕上)
            print(f"\033[96m{reply}\033[0m")    # 打印回应字体(青色)
            chat_win1.send_message(f"@{sender}"+ reply)                       # 把回应发送到qq
            chat_win1.message_processing_queues.pop(0)  # 清理回应的消息(出队)
            print(f"\033[94m已完成“{sender}”的消息处理\033[0m")
print("\033[31m已停止QQ监听回复和退出deepseek对话引擎\033[0m")
# {"发送者": "yan di fei","发送消息": "hello world","发送时间": "10:10:20"}


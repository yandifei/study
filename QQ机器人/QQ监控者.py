from QQScript.QQMessageMonitor import * # 导包
# qq_group_name = input("请输入监听的群聊:\n") # 猫猫       雁低飞
# qq_monitor_name = input("请输入你的身份(最好是聊天对象的名称，如你在q群的名称):\n")
qq_group_name = "鸣潮想睡觉"
qq_monitor_name = "雁低飞"
chat_win1 = QQMessageMonitor(qq_group_name, qq_monitor_name)    # 会自动置顶和自动展示(最小化显示)
chat_win1.show_win()    # 展示窗口
chat_win1.top_win()     # 置顶窗口
chat_win1.move()        # 把窗口移动到最上角 0,1010
print("窗口已放置最左上角并置顶，可通过鼠标拖拽拉伸")
print(f"数据存放路径:\t{chat_win1.message_data_txt}")
for one_message in chat_win1.message_list:  # 打印初次绑定后的消息
    print(one_message)
while True:
    sleep(0.5)  # 每0.5秒监测一次变化
    chat_win1.show_win()    # 展示窗口
    chat_win1.top_win()     # 置顶开窗口
    chat_win1.monitor_message() # 始监控

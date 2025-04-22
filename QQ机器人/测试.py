from QQScript.QQMessageMonitor import * # 导包
# qq_group_name = input("请输入监听的群聊:\n") # 猫猫       雁低飞
# qq_monitor_name = input("请输入你的身份(最好是聊天对象的名称，如你在q群的名称):\n")
qq_group_name = "猫猫"
qq_monitor_name = "雁低飞"
chat_win1 = QQMessageMonitor(qq_group_name, qq_monitor_name)
chat_win1.move(0,1010)  # 把窗口移动到最上角
print("窗口已放置最左上角，可通过鼠标拖拽拉伸")
print(f"数据存放路径:\t{chat_win1.message_data_txt}")
for one_message in chat_win1.message_list:  # 打印初次绑定后的消息
    print(one_message)
while True:
    sleep(1)  # 每1秒监测一次变化
    chat_win1.monitor_message()
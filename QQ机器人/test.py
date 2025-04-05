import uiautomation
from time import sleep
sleep(3)
qq_chat_window = uiautomation.WindowControl(searchDepth=1,Name="文件传输助手")
def get_message_list():
    message_list = list()
    message_control_list = qq_chat_window.ListControl().GetChildren()
    for message_control in message_control_list:
        message_list.append(message_control.Name)
    return message_list

former_msg_list = get_message_list()
while True:
    latest_msg_list = get_message_list()
    if latest_msg_list != former_msg_list:
        #当末条消息和上一条消息不同时
        new_msg = latest_msg_list[-1]
        print(new_msg)
        #----new_sg就是新的消息
        new_msg = get_message_list
    sleep(1)
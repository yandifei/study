"""QQ窗口消息监听
1.不使用OCR(字体识别获取聊天信息)
2.截获各种所有聊天记录(文本、图片、转发的聊天记录、表情包、链接等)
3.无封号风险、一键exe启动、自动回复、根据上下问回复
"""
import uiautomation as auto
from time import sleep
print("成功导入uiautomation")
# ->窗口
win = auto.GetRootControl()
##print(win)
win_childs = win.GetChildren()    # 获得根窗口
##qq_win = 0
##遍历根窗口的子窗口

chat_name = "鸣潮想睡觉"    # qq群聊窗口
for child in win_childs:
##    print(f"类名: {child.ClassName}\t标题: {child.Name}\t控件类型: {child.ControlTypeName}")
    if child.Name == chat_name:
       qq_root_win = child # ->窗口->qq顶级窗口
try:    
    print(f"QQ聊天窗口:{qq_root_win}")
except():
    raise "未找到此QQ群"
document = qq_root_win.GetChildren()[0] # ->窗口->qq顶级窗口->文档
if "Chrome_RenderWidgetHostHWND" != document.ClassName:
    raise ValueError("没有找到窗口，请将QQ显示出来")

print("-------------------------------进入文档层剔除没用的组-------------------------------")
print(document)
document = document.GetChildren()[0]   # ->窗口->qq顶级窗口->文档->组
print(document)
main_window = document.GetChildren()[1] # ->窗口->qq顶级窗口->文档->组->第二个组
print("-------------------------------进入对话交流的窗口控件-------------------------------")
print(main_window)  # 真正用户交流的窗口
print("-----------------------------------窗口控制按钮------------------------------------")
# ->窗口->qq顶级窗口->文档->组->第二个组->第一个组(窗口控制按钮)
window_controls = main_window.GetChildren()[0]
print(window_controls)
# ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分)
chat_win = main_window.GetChildren()[1]
print(chat_win)
print("------------------------------QQ菜单栏(群名、语音通话等)----------------------------")
### ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分) ->第一个组(总菜单栏)
menu_win = chat_win.GetChildren()[0]   # 总菜单栏
# ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分) ->第一个组(总菜单栏)->第二个组(群名和人数按钮)
left_meun = menu_win.GetChildren()[1]   # 去掉没用的组
left_meun = left_meun.GetChildren()[0]  # 群名和人数(按钮)
group_name = left_meun.GetChildren()[0] # 文本控件(群名)
print(group_name.Name)  # 打印群名
member_count = left_meun.GetChildren()[1] # 文本控件(群名)
print(member_count.Name)    # 打印群聊总人数
# ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分) ->第一个组(总菜单栏)->第三个组(语音通话等按钮)
menu_win = chat_win.GetChildren()[0]   # 总菜单栏
right_meun = menu_win.GetChildren()[2]   # 去掉没用的组
# ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分) ->第一个组(总菜单栏)->第三个组(语音通话按钮)->更多工具栏的组
more_tool_bar = right_meun.GetChildren()[0]    # 进入更多工具栏的组
# 更多工具栏下有6个组，组里面对应语音通话、视频通话、屏幕共享、群应用、邀请加群、展开菜单的按钮
# 每个控件按钮下面其实还有个图像，对应的应该是qq的语音通话、视频通话等按钮的图像
voice_call_button = more_tool_bar.GetChildren()[0]  # 进入子控件，到达组里面
voice_call_button = voice_call_button.GetChildren()[0]  # 到达控件：语音通话
print(voice_call_button.Name)   # 打印语音通话

video_call_button = more_tool_bar.GetChildren()[1]  # 进入子控件，到达组里面
video_call_button = video_call_button.GetChildren()[0]  # 到达控件：视频通话
print(video_call_button.Name)   # 打印视频通话

screen_share_toggle = more_tool_bar.GetChildren()[2]  # 进入子控件，到达组里面
screen_share_toggle = screen_share_toggle.GetChildren()[0]  # 到达控件：屏幕共享
print(screen_share_toggle.Name)   # 打印屏幕共享

screen_share_toggle = more_tool_bar.GetChildren()[3]  # 进入子控件，到达组里面
screen_share_toggle = screen_share_toggle.GetChildren()[0]  # 到达控件：群应用
print(screen_share_toggle.Name)   # 打印群应用

invite_to_group_button = more_tool_bar.GetChildren()[4]  # 进入子控件，到达组里面
invite_to_group_button = invite_to_group_button.GetChildren()[0]  # 到达控件：邀请加群
print(invite_to_group_button.Name)   # 打印邀请加群

more_actions_button = more_tool_bar.GetChildren()[4]  # 进入子控件，到达组里面
more_actions_button = more_actions_button.GetChildren()[0]  # 到达控件：展开菜单
print(more_actions_button.Name)   # 打印展开菜单
print("------------------------------消息列表、消息编辑器区域、群成员列表----------------------------")
### ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分) ->第二个组（消息列表、消息编辑器区域、群成员列表）
chat_win.GetChildren()[1]   # 除了标题栏、菜单栏外的其他区域
print(chat_win)
print("------------------------------------消息列表(群消息的读取)----------------------------------")
message_area = chat_win.GetChildren()[1]    # 进入消息区域
message_area = message_area.GetChildren()[0]    # 进入消息区域，进入组里面
print(message_area.LocalizedControlType)    # 主要
message_list = message_area.GetChildren()[2]    # 进入"消息列表"
print(message_list.Name)    # 消息列表
message_list = message_list.GetChildren()[0]    # 进入单个组里面
message_list = message_list.GetChildren()[0]    # 再次进入单个组里面
print(f"获得的最大消息条数:{len(message_list.GetChildren())}")  # 获得的消息条数
# 到了这一步后有许多组，对应的都是群友的消息，选择哪条消息后还要进入一个组(没用的组)


def jude_send_message(jude_type_message):
    """判断发送的是什么类型的消息
    jude_type_message : 单个控件(不是组)
    """
    if jude_type_message.Name == "表情":
                return "表情 "
    elif jude_type_message.Name == "图片":
            return "图片或表情包 "
    elif "语音" in jude_type_message.Name:    # 字符串里面有语音2个字
             return f"{jude_type_message.Name} " # 语音X音
    elif jude_type_message.LocalizedControlType == "文本":   # 发送者的文本消息
           return jude_type_message.Name

def split_senderName_message(member_message):
    """消息分割
    member_message : 组，这个组里仅仅有2个组
    这个组的第一个子组是发送者的名称，第二个是消息体
    """
    if len(member_message.GetChildren()) == 1:  # 时间没有嵌入消息里面去
        member_message = member_message.GetChildren()[0]   # 进入2个自组
    elif len(member_message.GetChildren()) == 2:# 时间嵌入消息里面去了，需要分割
        member_message = member_message.GetChildren()[1]
    else: raise ValueError("除了时间还有其他东西嵌入了该消息列表")
    member_message =  member_message.GetChildren()  # 获得2个组
    # 发送者
    if len(member_message) == 2:    # 一般都是2组(发送者和消息体)
        senderName = member_message[0]    # 发送者的组
        print(f"发送者:{senderName.Name}",end='    ')
    else:
        senderName = member_message[0]. GetChildren()# 消息撤回情况
        print(f"发送者:{senderName[0].Name}",end='')
        print(f"{senderName[1].Name}")
        return "消息撤回"   # 退出遍历
    # 发送消息
    send_message = member_message[1]    # 消息者的组
    if send_message.Name == "视频":
        print(f"发送消息:视频")
        return  "视频"    # 发送的是视频，检测到直接返回，因为无法继续解析
    send_message = send_message.GetChildren()[0]    # 进入组消息控件组
    all_type_message = send_message.GetChildren()   # 消息组里面的所有子控件(一般为文本)
    # 单类型消息
    if len(all_type_message) == 1 : # 只有一个组(用户真正发送的消息)
        send_message = send_message.GetChildren()[0]    # 进入文本控件
        if send_message.LocalizedControlType == "文本":
            print(f"发送消息:{send_message.Name}")  # 用户发送的是文本消息
        else:
            print(f"发送消息:{jude_send_message(send_message)}")  # 其他类型的消息
    # 多类型
    else:   # 发送的是链接、表情包之类的，组的形式，多个组
##        print("非文本消息(图片、表情、链接等)")
        a = ""
        print(f"发送消息:",end='')
##        condition = send_message.PropertyCondition(send_message.LocalizedControlType,"文本")
        # 使用FindAll，通过给定的条件获取指定的所有子控件
##        all_type_message = send_message.FindAll(TreeScope=send_message.TreeScope.Descendants,Condition=condition)
        for i in send_message.GetChildren():
            if len(i.GetChildren()) > 0:
                for i in i.GetChildren():
                    if len(i.GetChildren()) > 0:
                        for i in i.GetChildren():
                            if i.LocalizedControlType == "文本":print(i.Name,end='1')
                    if i.LocalizedControlType == "文本":print(i.Name,end='2')
            if i.LocalizedControlType == "文本":print(i.Name,end='3') # 本体消息
        print(a,end='')
            

##        try:
##            print(len(send_message.GetChildren()))  # send_message有三个控件
##        except():
##            print("无法获取")
##        compound_message = all_type_message[index].GetChildren()    # 获取多个组合框(不同类型文本的组件)
        print() # 换行
                
        
    


    

# 从最大下标开始逆序打印到0
for index in range(len(message_list.GetChildren())): # 打印最新的消息列表
    member_message = message_list.GetChildren()[index]    # 进入一个成员的消息区域
    member_message = member_message.GetChildren()[0]    # 剔除一个没用的组
    if len(member_message.GetChildren()) == 1: # 此时的下表只有0，成员消息
        split_senderName_message(member_message)
    elif len(member_message.GetChildren()) == 2:  # 时间和成员消息放到同一个框了
        send_time_area = member_message.GetChildren()[0]
        send_time = send_time_area.GetChildren()[0]
        print(f"消息时间:{send_time.Name}")    # 时间是嵌进成员里面去的，此时占用了原来的下标
        split_senderName_message(member_message)
        


    
    

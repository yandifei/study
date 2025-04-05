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

chat_name = "七彩虹笔记本"    # qq群聊窗口
for child in win_childs:
##    print(f"类名: {child.ClassName}\t标题: {child.Name}\t控件类型: {child.ControlTypeName}")
    if child.Name == chat_name:
       qq_root_win = child # ->窗口->qq顶级窗口
       
print(f"QQ聊天窗口:{qq_root_win}")
document = qq_root_win.GetChildren()[0] # ->窗口->qq顶级窗口->文档
if "Chrome_RenderWidgetHostHWND" != document.ClassName:
    raise ValueError("没有找到窗口，请将QQ显示出来")

print("-------------------------------进入文档层剔除没用的组-------------------------------")
print(document)
document = document.GetChildren()[0]   # ->窗口->qq顶级窗口->文档->组
main_window = document.GetChildren()[1] # ->窗口->qq顶级窗口->文档->组->第二个组
print(main_window)  # 真正用户交流的窗口
window_controls = main_window.GetChildren()[0]   # ->窗口->qq顶级窗口->文档->组->第二个组->第一个组(窗口控制按钮)
# ->窗口->qq顶级窗口->文档->组->第二个组->第二个组(除标题栏的部分)
chat_win = main_window.GetChildren()[1]
print(chat_win)

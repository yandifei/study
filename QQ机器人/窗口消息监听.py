"""对windows的窗口进行消息监听"""

import win32con
# 这里的消息监听本质是检测窗口变化(为了专业人员看懂，不是hook键盘等各种的消息事件监听)
import win32gui


class MessageMonitoring:
    def __init__(self, dialogue_window_hwnd):
        """监听窗口属性和行为的类
        :参数 dialogue_window_hwnd: 对话窗口的窗口句柄
        """
        self.dialogue_window_hwnd = dialogue_window_hwnd

    # def

# def callback(hwnd, msg, wparam, lparam):
#     # 当目标窗口接收到文本更新消息时触发
#     if msg == win32con.WM_SETTEXT:
#         text = win32gui.GetWindowText(hwnd)
#         print("文本更新:", text)
#     return True

# 查找QQ消息窗口句柄
# qq_hwnd = win32gui.FindWindow("TXGuiFoundation", "张三的聊天窗口")  # 类名可通过Spy++获取

# 设置钩子
# win32gui.SetWindowLong(132000, win32con.GWL_WNDPROC, callback)

# 保持监听
# while True:
#     sleep(1)

if __name__ == '__main__':
    text = win32gui.GetWindowText(1115062)
    print(text)



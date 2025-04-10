"""这个库用来监控QQ消息，监控Q群成员的消息，以及监听QQ好友的消息
内置判断是Q群还是QQ好友
"""
from time import sleep
import uiautomation
import win32gui


class QQMessageMonitor:
    def __init__(self):
        return


def move_win(hwnd, x, y, repaint=True):
    """移动窗口到指定位置
    hwnd ： 窗口的句柄
    x ： 窗口左上角的x坐标
    y ： 窗口左上角的y坐标
    repaint : 重新绘制窗口，默认打开
    """
    size = win32gui.GetWindowRect(hwnd) # 获取窗口左上角和右下角的坐标
    width, height = size[2] - size[0], size[3] - size[1]    # 计算窗口的大小
    win32gui.MoveWindow(hwnd, x, y, width, height, repaint)

if __name__ == '__main__':
    sleep(3)
    uiautomation.GetChildren()
    for i in uiautomation.GetChildren():
        print(i.Name)
    # a = None
    # root_win = uiautomation.GetRootControl()
    # qq_chat_win = root_win.GetChildren()
    # for i in qq_chat_win:
    #     # print(i.Name)
    #     if i.Name == "鸣潮自动刷声骸":
    #         a = i
    #         print(i.ProcessId)
    #         print(i.NativeWindowHandle)
    #
    # for i in a.GetChildren():
    #     print(i.LocalizedControlType)

    # move_win(2491710,1000,1000)
"""这个库用来监控QQ消息，监控Q群成员的消息，以及监听QQ好友的消息
内置判断是Q群还是QQ好友
"""
import uiautomation
import win32gui


class QQMessageMonitor:
    def __new__(cls):   # 构造器





    def __init__(self,win_name=None,monitor_name=None,win_hwnd=None):
        """
        :参数 win_name: 左上角窗口名字(如果有备注名就填备注名)
        :参数 monitor_name: QQ号或发送者的名字
        """
        self.win_name = str(win_name)    # 左上角窗口名字(如果有备注名就填备注名) 强制转为字符串
        self.monitor_name = str(monitor_name)   # 强制转为字符串
        self.win_hwnd = win_hwnd    # 窗口句柄
        self.parameter_validation() # 调用函数对参数进行校验

        """窗口相关"""




    def parameter_validation(self):
        if self.win_name is None:
            print("请填写聊天框的名字",end=" ")
        if self.monitor_name is None:
            print("请填写你的身份(群中的称号或QQ号或QQ名)", end=" ")
        print() # 换行

def top_window_traversal(out=False):   # 顶层窗口遍历
    """获得当前的根窗口
    参数：out   ： 默认false不打印
    返回值： visible_windows_object（list）     ：   桌面可见的列表
    """
    desktop = uiautomation.GetRootControl()  # 获取当前桌面对象
    if not out: print(f"{desktop.Name}的可见窗口为:")
    visible_windows = desktop.GetChildren()  # 获得当前桌面所有可见的窗口的对象
    visible_windows_object = list()     # 列表存放可见窗口的对象
    for visible_window in visible_windows:
        visible_windows_object.append(visible_window)   #   遍历存放可见窗口的对象
        # if visible_window.GetFirstChild()
    if not out:
        for window in visible_windows_object: print(window.Name)# 打印找到的窗口名
    return visible_windows_object

def get_qq_pid():
    qq_hwnd = win32gui.FindWindow("Chrome_RenderWidgetHostHWND", "Chrome Legacy Window")


if __name__ == '__main__':
    a = QQMessageMonitor()
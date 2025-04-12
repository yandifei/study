"""这个库用来监控QQ消息，监控Q群成员的消息，以及监听QQ好友的消息
内置判断是Q群还是QQ好友
"""
import uiautomation
import win32gui
import win32con

class QQMessageMonitor:
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
    """获得当前的根窗口的所有可见窗口
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
    """判断登录了多少个QQ   1. 把符合句柄的窗口展示出来 2. 通过结构判断是不是qq窗口
    返回值： qq_account : qq窗口句柄的列表
    """
    all_qq_hwnd = list()
    def enum_child(hwnd, _):    # 回调函数
        if not win32gui.IsWindowVisible(hwnd):  # 过滤不可见的窗口
            return True # 直接跳过
        if win32gui.GetClassName(hwnd) == "Chrome_WidgetWin_1" and win32gui.GetWindowText(hwnd) == "QQ":
             all_qq_hwnd.append(hwnd)  # 获得所有的qq类名和标题的句柄
        return True  # 继续遍历
    win32gui.EnumChildWindows(None, enum_child, None)   # 遍历函数
    print(all_qq_hwnd)
    """结构判断是否是QQ窗口"""
    qq_accounts = list() # 用来放置qq账号
    win32gui.ShowWindow(all_qq_hwnd[0], win32con.SW_SHOW)  # 展示QQ窗口
    for qq_hwnd in all_qq_hwnd:    # 遍历符合qq类名和标题的句柄
        for qq_win in top_window_traversal():
            if qq_win.Name == "QQ" and qq_win.LocalizedControlType == "窗格":
    #
    #
    #     qq_control = qq_control.GetChildren()[0] # 获得第一个控件(文档)02
    #     if qq_control.LocalizedControlType != "文档":
    #         raise EnvironmentError("无法定位窗口，请手动打开所有的QQ窗口放置到桌面上")
    #     qq_control = qq_control.GetFirstChildControl().GetFirstChildControl() # 进入2个组
    #     if len(qq_control.GetChildren()) == 4:  # 如果是q群或好友就只有一个子控件，qq有4个控件
    #         qq_accounts.append(qq_hwnd)
    # return qq_accounts






def jude_group_friend():
    """判断该对话框是QQ群还是qq好友(根据结构判断)
    """
    return




if __name__ == '__main__':
    # a = QQMessageMonitor()
    print(get_qq_pid())
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

def get_qq_win_hwnd():
    """判断登录了多少个QQ   1. 把符合句柄的窗口展示出来 2. 通过结构判断是不是qq窗口
    返回值： qq_win_hwnd : qq窗口句柄的列表
    """
    visible_windows = uiautomation.GetRootControl().GetChildren()  # 获取当前桌面对象->获得当前桌面所有可见的窗口的对象
    qq_win_hwnd = list() # 放置QQ号窗口句柄
    for visible_window in visible_windows:
        if visible_window.Name == "QQ" and visible_window.ClassName == "Chrome_WidgetWin_1":    # 检索类名和标题
            win32gui.SetWindowPos(visible_window.NativeWindowHandle,win32con.HWND_TOPMOST,
                                  0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE) # 窗口置顶
            if visible_window.GetChildren()[0].LocalizedControlType != "文档":    # 报错警告（没有文档对象）
                raise EnvironmentError("请手动把QQ窗口显示在桌面上")
            # 通过结构判断是QQ窗口还是对话窗口
            if len(visible_window.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()) == 4:   # 如果是QQ号则为4，对话窗口为1
                qq_win_hwnd.append(visible_window.NativeWindowHandle)   # 把十进制的qq窗口句柄放置在列表种
            win32gui.SetWindowPos(visible_window.NativeWindowHandle,win32con.HWND_NOTOPMOST,
                0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)# 取消置顶
    return qq_win_hwnd




def jude_group_friend():
    """判断该对话框是QQ群还是qq好友(根据结构判断)
    """
    return




if __name__ == '__main__':
    # a = QQMessageMonitor()
    print(get_qq_win_hwnd())
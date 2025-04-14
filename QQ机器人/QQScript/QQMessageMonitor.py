"""这个库用来监控QQ消息，监控Q群成员的消息，以及监听QQ好友的消息
内置判断是Q群还是QQ好友
"""
import uiautomation
import win32gui
import win32con
from time import sleep

class QQMessageMonitor:
    def __init__(self,win_name=None,monitor_name=None):
        """
        :参数 win_name: 左上角窗口名字(如果有备注名就填备注名)
        :参数 monitor_name: QQ号或发送者的名字
        """
        self.win_name = str(win_name)    # 左上角窗口名字(如果有备注名就填备注名) 强制转为字符串
        self.monitor_name = str(monitor_name)   # 强制转为字符串
        self.parameter_validation() # 调用函数对参数进行校验
        # 窗口相关
        self.visible_windows_object = self.top_window_traversal()   # 遍历顶层窗口
        self.find_qq_chat_win(self.visible_windows_object)   # 从顶层窗口中找到指定的qq聊天窗口


    def parameter_validation(self):
        """创建对象时对输入的信息进行校验"""
        if self.win_name is None:
            print("请填写聊天框的名字",end=" ")
        if self.monitor_name is None:
            print("请填写你的身份(群中的称号或QQ号或QQ名)", end=" ")
        print() # 换行

    @staticmethod
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
        if not out:
            for window in visible_windows_object: print(window.Name)# 打印找到的窗口名
        return visible_windows_object

    # 窗口相关

    def find_qq_chat_win(self,visible_windows_object):
        """遍历顶层窗口找到指定qq聊天窗口
        :参数 visible_windows_object: 可见窗口的列表
        :返回值:
        """
        qq_chat_win_list = list() # 如果标题和类名相同就拒绝绑定
        for visible_window in visible_windows_object:
            # 找到符合指定好友名或qq群名的窗口
            if visible_window.Name == self.win_name and visible_window.ClassName == "Chrome_WidgetWin_1":
                qq_chat_win_list.append(visible_window) # 把查找对象添加进去
        if len(qq_chat_win_list) == 0:
            raise ValueError("没有找到这个窗口")
        elif len(qq_chat_win_list) >= 2:
            raise ValueError("请确保当前名字的窗口没有重名")
        # 检查结构
        if self.is_qq(qq_chat_win_list[0]):


        









    @staticmethod
    def is_qq(obj):
        try:
            if len(obj.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()) == 4:
                return True
        except():
            raise ValueError("请把qq窗口置顶")
        return False

    def jude_group_friend(self,obj):
        """判断该对话框是QQ群还是qq好友(根据结构判断)
        """
        return



if __name__ == '__main__':
    # a = QQMessageMonitor()
    print(get_qq_win_hwnd())
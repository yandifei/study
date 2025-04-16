"""这个库用来监控QQ消息，监控Q群成员的消息，以及监听QQ好友的消息
内置判断是Q群还是QQ好友
"""
import uiautomation
import win32gui
import win32con
from time import sleep

class QQMessageMonitor:
    def __init__(self,win_name="",monitor_name=""):
        """
        :参数 win_name: 左上角窗口名字(如果有备注名就填备注名)
        :参数 monitor_name: QQ号或发送者的名字
        """
        self.win_name = str(win_name)    # 左上角窗口名字(如果有备注名就填备注名) 强制转为字符串
        self.monitor_name = str(monitor_name)   # 强制转为字符串
        self.parameter_validation() # 调用函数对参数进行校验
        # 窗口初始化相关
        self.group_or_friend = None # 记录窗口QQ群还是好友
        self.qq_chat_win = self.find_qq_chat_win(self.top_window_traversal())   # 遍历顶层窗口->从顶层窗口中找到指定的qq聊天窗口
        self.qq_chat_hwnd = self.qq_chat_win.NativeWindowHandle # 被监听窗口的句柄
        self.cancel_top_win()   # 取消窗口置顶，防止窗口置顶失效
        self.top_win()  # 把窗口置顶，防止窗口被遮挡导致渲染停止无法监控窗口
        self.top_wait_time = 1  # 设置置顶后等待qq渲染完成的属性，（如果电脑卡的话可以调大属性）
        sleep(self.top_wait_time)    # 等待1秒窗口完全置顶（qq置顶后渲染需要时间）
        self.pid = self.qq_chat_win.ProcessId   # 被监听窗口的进程ID
        self.geometry = self.qq_chat_win.BoundingRectangle  # 窗口的位置和大小
        print(f"成功绑定“{win_name}”{self.jude_group_or_friend(self.qq_chat_win)}窗口并置顶窗口\t监听者：{monitor_name}")# 把对象进行绑定，动态属性修改并打印
        print(f"“{win_name}”句柄:{self.qq_chat_hwnd}\t进程ID:{self.pid}\t窗口大小:{self.geometry}")
        """聊天窗口控制监控相关"""
        # 文档->组->组2(子孩子有2个组，第一个组是窗口控制按钮相关，第二个组是非窗口控制按钮的界面)
        self.main_chat_win = self.qq_chat_win.GetChildren()[0].GetChildren()[0].GetChildren()[1]
        # 文档->组->组2->组2(好友有2个组，群有3个组)可以用来区分qq还是群
        # 标题栏(title_bar)[窗口控制按钮]
        self.top_button = self.main_chat_win.GetChildren()[0].GetChildren()[0]  #置顶（复合按钮）按钮
        self.min_button = self.main_chat_win.GetChildren()[0].GetChildren()[1]  # 最小化按钮
        self.max_button = self.main_chat_win.GetChildren()[0].GetChildren()[2]  # 最大化按钮
        self.close_button = self.main_chat_win.GetChildren()[0].GetChildren()[3]    # 关闭按钮
        # 标题栏(menu_bar)[菜单标题(好友名或群名和人数)、菜单选项按钮]
        # 2个组里面->组2->组1->组2->好友名或群名按钮->有2个组（1个是群名，一个是人数）
        self.menu_bar_button = self.main_chat_win.GetChildren()[1].GetChildren()[0].GetChildren()[1]    # 按钮
        self.menu_bar_name = self.main_chat_win.GetChildren()[1].GetChildren()[0].GetChildren()[1].GetChildren()[0] # 群名
        self.menu_bar_name = self.main_chat_win.GetChildren()[1].GetChildren()[0].GetChildren()[1].GetChildren()[1] # 人数
        # 2个组里面->组2->组1->组3->"更多"工具栏->6个组都菜单栏选项按钮（6个组里面对应语音通话、视频通话、屏幕共享、群应用、邀请加群、展开菜单的按钮）
        self.menu_option_buttons  =self.main_chat_win.GetChildren()[1].GetChildren()[0].GetChildren()[2].GetChildren()[0]
        self.voice_call_button = self.menu_option_buttons.GetChildren()[0].GetChildren()[0] # 语音通话
        self.voice_call_button = self.menu_option_buttons.GetChildren()[1].GetChildren()[0] # 视频通话
        self.voice_call_button = self.menu_option_buttons.GetChildren()[2].GetChildren()[0] # 屏幕共享
        self.voice_call_button = self.menu_option_buttons.GetChildren()[3].GetChildren()[0] # 群应用
        self.voice_call_button = self.menu_option_buttons.GetChildren()[4].GetChildren()[0] # 邀请加群
        self.voice_call_button = self.menu_option_buttons.GetChildren()[5].GetChildren()[0] # 展开菜单的按钮
        """消息列表框(message_list_box)"""
        # 2个组里面->组2->组2->组1->组3->组0->组0->全是消息控件，需要解析
        self.message_list_box = self.main_chat_win.GetChildren()[1].GetChildren()[2].GetChildren()[0].GetChildren()[2].GetChildren()[2].GetChildren()[0].GetChildren()[0]
        """编辑工具栏(edit_tool_bar)"""
        self.edit_tool_bar = self.main_chat_win.GetChildren()[1].GetChildren()[2]




    def parameter_validation(self):
        """创建对象时对输入的信息进行校验"""
        if self.win_name == "":
            raise ValueError("请填写聊天框的名字")
        elif self.win_name == "QQ":
            raise ValueError("检测到需要监听的窗口名是QQ，请改备注名")
        if self.monitor_name == "":
            raise ValueError("请填写你的身份(群中的称号或QQ号或QQ名)")


    # 窗口遍历查找相关
    @staticmethod
    def refind(obj):
        """刷新控件，1.控件发生变化就需要刷新 2.建立新的窗口时也要刷新
        参数：obj：传入刷新对象
        """
        obj.Refind()  # 刷新控件

    @staticmethod
    def top_window_traversal(out=False):   # 顶层窗口遍历
        """获得当前的根窗口的所有可见窗口
        参数：out   ： 默认false不打印
        返回值： visible_windows_object（list）     ：   桌面可见的列表
        """
        desktop = uiautomation.GetRootControl()  # 获取当前桌面对象
        if out: print(f"{desktop.Name}的可见窗口为:")
        visible_windows = desktop.GetChildren()  # 获得当前桌面所有可见的窗口的对象
        visible_windows_object = list()     # 列表存放可见窗口的对象
        for visible_window in visible_windows:
            visible_windows_object.append(visible_window)   #   遍历存放可见窗口的对象
        if out:
            for window in visible_windows_object: print(window.Name)# 打印找到的窗口名
        return visible_windows_object
    
    
    
    # def message_list(self):
    #     # 文档->组->组2->组2->组2->组1->组3-组1->组 后面的孩子就是一条条的消息窗口了
    #     a = self.qq_chat_win.GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()[1].GetChildren()[0].GetChildren()[2].GetChildren()[0].GetChildren()[0]



    # 窗口控制相关
    def find_qq_chat_win(self,visible_windows_object):
        """遍历顶层窗口找到指定qq聊天窗口
        :参数 visible_windows_object: 可见窗口的列表
        :返回值:指定窗口的对象
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
        return qq_chat_win_list[0]

    @staticmethod
    def is_qq(obj):
        """检测是不是qq窗口的结构
        参数：obj ：需要判断的对象
        返回值：False 或 True
        """
        try:
            if len(obj.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()) == 4:
                return True
        except():
            raise ValueError("请把qq窗口置顶并展示在在桌面上")
        return False

    def jude_group_or_friend(self,obj):
        """判断该对话框是QQ群还是qq好友(根据结构判断)
        参数：obj：窗口的对象
        返回值： "群聊" 或 "好友"
        会该变self.group_or_friend属性
        """
        # 检查结构（不需要担心是QQ窗口，考虑qq群还是qq好友就行）
        # obj.Refind()    # 刷新控件
        if obj.GetChildren()[0].LocalizedControlType != "文档":
            # sleep(1)
            print(obj.GetChildren()[0].LocalizedControlType)
            print(obj.GetChildren()[1].LocalizedControlType)
            raise EnvironmentError(f"请把“{self.win_name}”窗口显示在桌面上")
        # 文档->组->第二个组->第二个组->群聊3个|好友2个组
        elif len(obj.GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()) == 3:
            self.group_or_friend = "群聊"
            return "群聊"
        elif len(obj.GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()) == 2:
            self.group_or_friend = "好友"
            return "好友"

    def move(self,x, y,repaint=True):
        """qq聊天窗口位置移动
        x ： 窗口左上角的x坐标
        y ： 窗口左上角的y坐标
        repaint : 重新绘制窗口，默认打开
        """
        size = win32gui.GetWindowRect(self.qq_chat_hwnd)  # 获取窗口左上角和右下角的坐标
        width, height = size[2] - size[0], size[3] - size[1]    # 计算窗口的大小
        win32gui.MoveWindow(self.qq_chat_hwnd, x, y, width, height, repaint)

    def set_size(self, width, height, repaint=True):
        """改变qq聊天窗口的大小（坐标保持在左上角）
        width ： 设置窗口的宽度
        height ： 设置窗口的高度
        repaint : 重新绘制窗口，默认打开
        """
        point = win32gui.GetWindowRect(self.qq_chat_hwnd)  # 获取窗口左上角和右下角的坐标
        win32gui.MoveWindow(self.qq_chat_hwnd, point[0], point[1], width, height, repaint)

    def top_win(self):
        """将qq聊天窗口置顶"""
        win32gui.SetWindowPos(
            self.qq_chat_hwnd,
            win32con.HWND_TOPMOST,  # 置顶层
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

    def cancel_top_win(self):
        """取消窗口置顶
        hwnd ： 窗口的句柄
        """
        win32gui.SetWindowPos(
            self.qq_chat_hwnd,
            win32con.HWND_NOTOPMOST,  # 取消置顶
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

if __name__ == '__main__':
    # a = QQMessageMonitor()
    chat2 = QQMessageMonitor("蓝宝", "雁低飞")
    chat2.cancel_top_win()
    chat1 = QQMessageMonitor("鸣潮自动刷声骸","雁低飞")
    chat1.cancel_top_win()
    # chat3 = QQMessageMonitor("七彩虹笔记本", "雁低飞")
    # chat3.cancel_top_win()
